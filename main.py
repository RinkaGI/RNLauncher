# from tkinter import Tk, Label, Entry, Button, mainloop
# from tkinter.ttk import Combobox

import minecraft_launcher_lib as mclib
import subprocess
import sys
import hashlib

def getMinecraftDir():
    return mclib.utils.get_minecraft_directory()

def installMinecraft(version):
    return mclib.install.install_minecraft_version(version, mclib.utils.get_minecraft_directory())

def launchMinecraft(version, options):
    return mclib.command.get_minecraft_command(version, mclib.utils.get_minecraft_directory(), options)

def getAvalaibleVersions():
    ver = mclib.utils.get_available_versions(mclib.utils.get_minecraft_directory())
    listVersions = []
    for i in ver:
        listVersions.append(i['id'])
    return listVersions

import hashlib
import flet as ft

def main(page: ft.Page):
    page.title = "RNLauncher"
    versionList = []

    def forgeInstall(e):
            forgeV = mclib.forge.find_forge_version(versionEntry.value)
        
            if forgeV is None:
                forgeNoVersiondlg = ft.AlertDialog(
                    title = ft.Text("This version is not supported by Forge")
                )
                page.dialog = forgeNoVersiondlg
                forgeNoVersiondlg.open = True
                page.update()

            mclib.forge.run_forge_installer(forgeV)
            
            page.update()

    usernameEntry = ft.TextField()
    jvmramEntry = ft.TextField(value=2)
    forgeEntry = ft.ElevatedButton("Install Forge", on_click=forgeInstall)
    for i in mclib.utils.get_installed_versions(mclib.utils.get_minecraft_directory()):
        versionList.append(ft.dropdown.Option(i["id"]))
    for i in getAvalaibleVersions():
        versionList.append(ft.dropdown.Option(i))
    versionEntry = ft.Dropdown(options=versionList)

    dlg = ft.AlertDialog(
        title = ft.Text("Loading some things (will take time if the version is not installed)")
    )
    errordlg = ft.AlertDialog(
        title = ft.Text("There is a problem with this version, try again with other Minecraft Version")
    )

    config = {
        "username": usernameEntry.value,
        "uuid": str(hashlib.md5(str.encode(usernameEntry.value)).digest()),
        "token": "",
        "launcherName": "RNLauncher",
        "gameDirectory": getMinecraftDir(),
        "jvmArguments": [f"-Xmx{jvmramEntry.value}G"]
    }

    def launch(e):
        try:
            mc = launchMinecraft(versionEntry.value, config)
            page.dialog = dlg
            dlg.open = True
            page.update()
            subprocess.call(mc)
            page.window_destroy()
            sys.exit(0)
        except:
            page.dialog = errordlg
            errordlg.open = True
            page.update()

    page.add(
        # Title
        ft.Row(
            [
                ft.Image("./logo.png")
            ], alignment="center"
        ),
        
        ft.Row(
            [
                ft.Text("RNLauncher", font_family="Calibri", size=24)
            ], alignment="center"
        ),

        ft.Row(
            [
                ft.Text("Made with ❤ by RinkaDev", font_family="Arial", size=12)
            ], alignment="center", 
        ),

        ft.Divider(),

        ft.Row(
            [
                ft.Text("Username: ", size=16),
                usernameEntry
            ], alignment="center"
        ),

        ft.Divider(),

        ft.Row(
            [
                ft.Text("Version: ", size="16"),
                versionEntry,
                forgeEntry
            ], alignment="center"
        ),

        ft.Row(
            [
                ft.Text("JVM Max RAM: ", size=16),
                jvmramEntry
            ], alignment="center"
        ),

        ft.Divider(),

        ft.Row(
            [
                ft.FilledButton("Launch Minecraft!", on_click=launch)
            ], alignment="center"
        )
    )

ft.app(target=main)