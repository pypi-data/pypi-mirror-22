# -*- coding: utf-8 -*-
"""
Récupérer des mails d'étudiants en pièce jointe (1:1)
=====================================================

Récupère des fichiers en pièce jointe provenant d'étudiants comme un rendu de projet.
Le programme suppose qu'il n'y en a qu'un par étudiant, que tous les mails ont été
archivés dans un répertoire d'une boîte de message, ici gmail.
Il faut supprimer le contenu du répertoire pour mettre à jour l'ensemble
des projets. Dans le cas contraire, le code est prévu pour mettre à jour le répertoire
à partir des derniers mails recensés dans le fichiers *mails.txt*.

.. _script-fetch-students-projets-py:
"""

#########################################
# import
import sys
import os
import pandas
import keyring

#################################
# paramètres de la récupération
# tous les mails doivent être dans le même répertoire

server = "imap.gmail.com"
mailfolder = ["ensae/actuariat"]
date = "10-Feb-2017"
do_mail = True
dest_folder = os.path.normpath(os.path.abspath(os.path.join(
    *([os.path.dirname(__file__)] + ([".."] * 5) + ["_data", "ecole", "ENSAE", "2016-2017", "actuariat"]))))
print("dest", dest_folder)
filename_zip = os.path.join(dest_folder, "DM_2017.zip")
filename_mails = os.path.join(dest_folder, "emails.txt")
filename_excel = os.path.join(dest_folder, "DM_2017.xlsx")

#########################################
# create the folder if it does not exist

if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

#########################################
# Cette section ajoute des chemins pour des modules que je développe
# et que je n'installe jamais. Je pourrais me servir d'un environnement
# virtuel mais en pratique, c'est toujours un peu compliqué
# de mettre le mettre à jour en permanence.

this = os.path.abspath(os.path.dirname(__file__))
if "actuariat_python" in this:
    this = this.split("actuariat_python")[0].rstrip("\\/")
for module in ["jyquickhelper", "pyquickhelper", "pyensae",
               "pyrsslocal", "pymmails", "pymyinstall",
               "ensae_teaching_cs"]:
    try:
        exec("import %s" % module)
    except ImportError:
        p = os.path.join(this, module, "src")
        print("add path", p)
        sys.path.append(p)
        exec("import %s" % module)


#########################################
# logging

from pyquickhelper.loghelper import fLOG  # fetch_student_projects_from_gmail
fLOG(OutputPrint=True)


#########################################
# import des fonctions dont on a besoin

from ensae_teaching_cs.automation_students import ProjectsRepository, grab_addresses
from pyquickhelper.filehelper import encrypt_stream
from pymmails import MailBoxImap, EmailMessageRenderer, EmailMessageListRenderer
from pymmails.render.email_message_style import template_email_html_short


###########
# Settings
# On utilise keyring pour récupérer des mots de passe.

user = keyring.get_password("gmail", os.environ["COMPUTERNAME"] + "user")
pwd = keyring.get_password("gmail", os.environ["COMPUTERNAME"] + "pwd")
password = keyring.get_password("enc", os.environ["COMPUTERNAME"] + "pwd")
if user is None or pwd is None or password is None:
    print("ERROR: password or user or crypting password is empty, you should execute:")
    print(
        '    keyring.set_password("gmail", os.environ["COMPUTERNAME"] + "user", "..")')
    print(
        '    keyring.set_password("gmail", os.environ["COMPUTERNAME"] + "pwd", "..")')
    print(
        '    keyring.set_password("enc", os.environ["COMPUTERNAME"] + "pwd", "..")')
    print("Exit")
    sys.exit(0)

password = bytes(password, "ascii")


###########
# les adresses à éviter car
skip_address = [
    "xavier.dupre@gmail.com",
    "Xavier.Dupre@ensae.fr",
]

###############
# gather mails

fLOG("fetch mails")

if os.path.exists(filename_mails):
    with open(filename_mails, "r", encoding="utf8") as f:
        lines = f.readlines()
    emails = [l.strip("\r\t\n ") for l in lines]
else:
    box = MailBoxImap(user, pwd, server, ssl=True, fLOG=fLOG)
    box.login()
    emails = grab_addresses(box, mailfolder, date, fLOG=fLOG)
    box.logout()
    emails = list(sorted(set([_.strip("<>").lower()
                              for _ in emails if _ not in skip_address])))

    with open(filename_mails, "w", encoding="utf8") as f:
        f.write("\n".join(emails))

#####################
# create a dataframe

import pandas
rows = [{"nom_prenom": mail, "sujet": "DM", "groupe": i + 1}
        for i, mail in enumerate(emails)]
df = pandas.DataFrame(rows)
fLOG("dataframe", df.shape)
if df.shape[0] == 0:
    raise Exception("empty set")
df.to_excel(filename_excel)

##################################
# create folders for each student

mappings = {}
folder = dest_folder

proj = ProjectsRepository(folder, fLOG=fLOG)
groups = proj.Groups
if do_mail or len(groups) < 10:
    fLOG("creation")
    proj = ProjectsRepository.create_folders_from_dataframe(df, folder,
                                                            col_subject="sujet", fLOG=fLOG, col_group="groupe",
                                                            col_student="nom_prenom",
                                                            email_function=emails, skip_if_nomail=False,
                                                            must_have_email=True)
fLOG("nb groups", len(proj.Groups))

#############
# dump mails

if do_mail:
    email_render = EmailMessageRenderer(
        tmpl=template_email_html_short, fLOG=fLOG)
    render = EmailMessageListRenderer(title="list of mails",
                                      email_renderer=email_render, fLOG=fLOG)

    box = MailBoxImap(user, pwd, server, ssl=True, fLOG=fLOG)
    box.login()
    mails = proj.dump_group_mails(render, group=None,
                                  mailbox=box, subfolder=mailfolder, date=date,
                                  overwrite=False, convert_files=True)
    box.logout()

################
# write summary

if True:
    fLOG("summary")
    index = os.path.join(dest_folder, "index.html")
    if os.path.exists(index):
        os.remove(index)
    proj.write_summary()


#################
# zip everything

if True:
    if os.path.exists(filename_zip):
        os.remove(filename_zip)
    proj.zip_group(None, filename_zip,
                   addition=[index, os.path.join(dest_folder, "mail_style.css"),
                             filename_excel, filename_mails])

############
# encryption

if True:
    fLOG("encryption")
    enc = filename_zip.replace(".zip", ".enc")
    encrypt_stream(password, filename_zip, enc, chunksize=2**30)
