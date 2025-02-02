import discord
from discord import app_commands

SCHWESTER_ROLE = "Schwester"
BRUDER_ROLE = "Bruder"
MITGLIED_ROLE = "Mitglied"
ALLOWED_VERIFIER_ROLES = ["Verifizierer", "Verifiziererin"]

# Slash-Command: verify-schwester
@app_commands.command(name="verify-schwester", description="Weist einem Benutzer die Rolle 'Schwester' und 'Mitglied' zu.")
async def verify_schwester(interaction: discord.Interaction, user: discord.Member):
    # Berechtigungen prüfen
    executor_roles = [r.name for r in interaction.user.roles]
    if not any(r in ALLOWED_VERIFIER_ROLES for r in executor_roles):
        await interaction.response.send_message(
            "Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True
        )
        return

    # Rollen abrufen
    guild = interaction.guild
    schwester_role = discord.utils.get(guild.roles, name=SCHWESTER_ROLE)
    mitglied_role = discord.utils.get(guild.roles, name=MITGLIED_ROLE)

    if not schwester_role or not mitglied_role:
        await interaction.response.send_message(
            "Eine oder mehrere benötigte Rollen existieren nicht auf diesem Server.", ephemeral=True
        )
        return

    try:
        await user.add_roles(schwester_role, mitglied_role)

        # Entfernen der "Unverifiziert" Rollen
        roles_to_remove = ["Unverifiziert", "Unverifiziert W"]
        for role_name in roles_to_remove:
            role_to_remove = discord.utils.get(guild.roles, name=role_name)
            if role_to_remove and role_to_remove in user.roles:
                await user.remove_roles(role_to_remove)

        await interaction.response.send_message(
            f"Die Rollen '{SCHWESTER_ROLE}' und '{MITGLIED_ROLE}' wurden erfolgreich {user.mention} zugewiesen!"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "Ich habe nicht die Berechtigung, diese Rollen zuzuweisen.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"Ein Fehler ist aufgetreten: {e}", ephemeral=True
        )

# Slash-Command: verify-bruder
@app_commands.command(name="verify-bruder", description="Weist einem Benutzer die Rolle 'Bruder' und 'Mitglied' zu.")
async def verify_bruder(interaction: discord.Interaction, user: discord.Member):
    # Berechtigungen prüfen
    executor_roles = [r.name for r in interaction.user.roles]
    if not any(r in ALLOWED_VERIFIER_ROLES for r in executor_roles):
        await interaction.response.send_message(
            "Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True
        )
        return

    # Rollen abrufen
    guild = interaction.guild
    bruder_role = discord.utils.get(guild.roles, name=BRUDER_ROLE)
    mitglied_role = discord.utils.get(guild.roles, name=MITGLIED_ROLE)

    if not bruder_role or not mitglied_role:
        await interaction.response.send_message(
            "Eine oder mehrere benötigte Rollen existieren nicht auf diesem Server.", ephemeral=True
        )
        return

    try:
        await user.add_roles(bruder_role, mitglied_role)

        # Entfernen der "Unverifiziert" Rollen
        roles_to_remove = ["Unverifiziert", "Unverifiziert M"]
        for role_name in roles_to_remove:
            role_to_remove = discord.utils.get(guild.roles, name=role_name)
            if role_to_remove and role_to_remove in user.roles:
                await user.remove_roles(role_to_remove)

        await interaction.response.send_message(
            f"Die Rollen '{BRUDER_ROLE}' und '{MITGLIED_ROLE}' wurden erfolgreich {user.mention} zugewiesen!"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "Ich habe nicht die Berechtigung, diese Rollen zuzuweisen.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"Ein Fehler ist aufgetreten: {e}", ephemeral=True
        )


class VerificationButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def disable_buttons_for_user_if_verified(self, interaction: discord.Interaction):
        """Überprüft dynamisch die Rolle und deaktiviert Buttons nur, wenn nötig."""
        role_unverifiziert = discord.utils.get(interaction.guild.roles, name="Unverifiziert")
        if role_unverifiziert not in interaction.user.roles:
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await interaction.message.edit(view=self)

    @discord.ui.button(label="♂️ Muslim", style=discord.ButtonStyle.blurple, custom_id="muslim_button")
    async def muslim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_unverifiziert = discord.utils.get(interaction.guild.roles, name="Unverifiziert")
        role_muslim = discord.utils.get(interaction.guild.roles, name="Unverifiziert M")
        guild = interaction.guild
        target_channel = discord.utils.get(guild.channels, id=1335335933373059163)

        if role_unverifiziert in interaction.user.roles:
            await interaction.user.add_roles(role_muslim)
            await interaction.response.send_message(
                f"Du hast die Rolle 'Unverifiziert M' erhalten! Bitte fahre hier fort: {target_channel.mention}",
                ephemeral=True
            )
            await interaction.user.remove_roles(role_unverifiziert)
            await self.disable_buttons_for_user_if_verified(interaction)
        else:
            await interaction.response.send_message("Du hast bereits dein Geschlecht ausgewählt. Hast du einen Fehler gemacht? Dann schildere die Situation innerhalb des Tickets.", ephemeral=True)

    @discord.ui.button(label="♀️ Muslima", style=discord.ButtonStyle.red, custom_id="muslima_button")
    async def muslima_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_unverifiziert = discord.utils.get(interaction.guild.roles, name="Unverifiziert")
        role_muslima = discord.utils.get(interaction.guild.roles, name="Unverifiziert W")
        guild = interaction.guild
        target_channel = discord.utils.get(guild.channels, id=1335337143136157696)

        if role_unverifiziert in interaction.user.roles:
            await interaction.user.add_roles(role_muslima)
            await interaction.response.send_message(
                f"Du hast die Rolle 'Unverifiziert W' erhalten! Bitte fahre hier fort: {target_channel.mention}",
                ephemeral=True
            )
            await interaction.user.remove_roles(role_unverifiziert)
            await self.disable_buttons_for_user_if_verified(interaction)
        else:
            await interaction.response.send_message("Du hast bereits dein Geschlecht ausgewählt. Hast du einen Fehler gemacht? Dann schildere die Situation innerhalb des Tickets.", ephemeral=True)

    @discord.ui.button(label="📩 Ich habe Interesse am Islam", style=discord.ButtonStyle.green, custom_id="interest_button")
    async def interest_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_unverifiziert = discord.utils.get(interaction.guild.roles, name="Unverifiziert")
        role_interessiert = discord.utils.get(interaction.guild.roles, name="Interessiert")
        # Der Channel, in dem der Benutzer fortfahren soll
        channel = interaction.guild.get_channel(1335340894660071524)

        if role_unverifiziert in interaction.user.roles:
            # Rolle "Interessiert" hinzufügen und "Unverifiziert" entfernen
            await interaction.user.add_roles(role_interessiert)
            await interaction.user.remove_roles(role_unverifiziert)

            # Ephemeral-Nachricht zur Bestätigung und Hinweis auf den Channel
            await interaction.response.send_message(
                f"Du hast jetzt die Rolle 'Interessiert'. Bitte fahre im {channel.mention} fort, um mit den nächsten Schritten fortzufahren.",
                ephemeral=True
            )

            # Falls gewünscht, kannst du hier zusätzliche Logik einfügen,
            # um Buttons zu deaktivieren oder den Status des Benutzers zu aktualisieren.
            await self.disable_buttons_for_user_if_verified(interaction)
        else:
            await interaction.response.send_message("Du bist bereits verifiziert oder hast dich bereits gemeldet.", ephemeral=True)




# Setup-Verification-Befehl
@app_commands.command(name="setup_verification", description="Richtet die Verifizierung mit Buttons ein.")
async def setup_verification(interaction: discord.Interaction):
    # Embed für Verifizierungstext
    embed = discord.Embed(
        title="🔒 Verifizierung",
        description=(
            "Bitte wähle zur Verifizierung:\n\n"
            "Bist du Muslim oder Muslima❓\n"
            "Dann wähle dein Geschlecht aus.\n\n"
            "Ansonsten:\n"
            "Hast du Interesse am Islam❓\n\n"
            "Klicke einfach auf den entsprechenden Button, um fortzufahren❗"
        ),
        color=discord.Color.blue()
    )
    
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1335345553197895732/1335346062004588544/Amanah_Logo_Animation.gif?ex=679fd56e&is=679e83ee&hm=018d10ee799f1c8a21de29341f1f0e546c566b2a45d2fd19d7f5ac08b9299b0a&=&width=1355&height=1355")

    # Nachricht mit Buttons senden
    await interaction.channel.send(embed=embed, view=VerificationButtons())
    await interaction.response.send_message("Verifizierung wurde eingerichtet!", ephemeral=True)

# Slash Command zum Hinzufügen eines Nutzers zu einem Thread
@app_commands.command(name="ticket-add", description="Fügt einen Benutzer zu einem Thread hinzu.")
async def ticket_add(interaction: discord.Interaction, user: discord.Member):  # Ändere den Typ zu str
    # Berechtigungen prüfen
    allowed_roles = ["Server Manager", "Admin+", "Admin", "Admina", "Server Architekt", "Mod"]
    executor_roles = [role.name for role in interaction.user.roles]
    if not any(role in allowed_roles for role in executor_roles):
        await interaction.response.send_message(
            "Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True
        )
        return

    # Kanal prüfen
    channel = interaction.channel
    if not isinstance(channel, (discord.TextChannel, discord.Thread)):
        await interaction.response.send_message(
            "Dieser Befehl kann nur in Textkanälen oder Threads verwendet werden.", ephemeral=True
        )
        return

    # Benutzer zu einem Kanal/Thread hinzufügen
    try:
        # Rechte setzen: Nachrichten lesen, senden und Historie einsehen
        await channel.set_permissions(user, 
            read_messages=True, 
            send_messages=True, 
            read_message_history=True
        )
        await interaction.response.send_message(
            f"{user.mention} wurde erfolgreich zu {channel.mention} hinzugefügt!"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "Ich habe nicht die Berechtigung, diesen Benutzer hinzuzufügen.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"Ein Fehler ist aufgetreten: {e}", ephemeral=True
        )