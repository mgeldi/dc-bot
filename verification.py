import discord
from discord import app_commands

SCHWESTER_ROLE = "Schwester"
BRUDER_ROLE = "Bruder"
ALLOWED_SCHWESTER_ROLES = ["Owner", "Admin+", "Admin", "Admina"]
ALLOWED_BRUDER_ROLES = ["Owner", "Admin+", "Admin"]

# Slash-Command: verify-schwester
@app_commands.command(name="verify-schwester", description="Weist einem Benutzer die Rolle 'Schwester' zu.")
async def verify_schwester(interaction: discord.Interaction, user: discord.Member):
    # Berechtigungen prüfen
    executor_roles = [r.name for r in interaction.user.roles]
    if not any(r in ALLOWED_SCHWESTER_ROLES or r.startswith("Verifiziererin") for r in executor_roles):
        await interaction.response.send_message(
            "Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True
        )
        return

    # Überprüfen, ob die Rolle existiert
    guild_role = discord.utils.get(interaction.guild.roles, name=SCHWESTER_ROLE)
    if guild_role is None:
        await interaction.response.send_message(
            f"Die Rolle '{SCHWESTER_ROLE}' existiert nicht auf diesem Server.", ephemeral=True
        )
        return

    # Zuweisung der Rolle
    try:
        await user.add_roles(guild_role)

        # Entfernen der Rolle "Unverifiziert" und ähnliche Rollen
        roles_to_remove = ["Unverifiziert", "Unverifiziert W"]
        for role_name in roles_to_remove:
            role_to_remove = discord.utils.get(interaction.guild.roles, name=role_name)
            if role_to_remove and role_to_remove in user.roles:
                await user.remove_roles(role_to_remove)

        await interaction.response.send_message(
            f"Die Rolle '{SCHWESTER_ROLE}' wurde erfolgreich {user.mention} zugewiesen!"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "Ich habe nicht die Berechtigung, diese Rolle zuzuweisen.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"Ein Fehler ist aufgetreten: {e}", ephemeral=True
        )

# Slash-Command: verify-bruder
@app_commands.command(name="verify-bruder", description="Weist einem Benutzer die Rolle 'Bruder' zu.")
async def verify_bruder(interaction: discord.Interaction, user: discord.Member):
    # Berechtigungen prüfen
    executor_roles = [r.name for r in interaction.user.roles]
    if not any(r in ALLOWED_BRUDER_ROLES or r.startswith("Verifizierer") for r in executor_roles):
        await interaction.response.send_message(
            "Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True
        )
        return

    # Überprüfen, ob die Rolle existiert
    guild_role = discord.utils.get(interaction.guild.roles, name=BRUDER_ROLE)
    if guild_role is None:
        await interaction.response.send_message(
            f"Die Rolle '{BRUDER_ROLE}' existiert nicht auf diesem Server.", ephemeral=True
        )
        return

    # Zuweisung der Rolle
    try:
        await user.add_roles(guild_role)

        # Entfernen der Rolle "Unverifiziert" und ähnliche Rollen
        roles_to_remove = ["Unverifiziert", "Unverifiziert M"]
        for role_name in roles_to_remove:
            role_to_remove = discord.utils.get(interaction.guild.roles, name=role_name)
            if role_to_remove and role_to_remove in user.roles:
                await user.remove_roles(role_to_remove)

        await interaction.response.send_message(
            f"Die Rolle '{BRUDER_ROLE}' wurde erfolgreich {user.mention} zugewiesen!"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "Ich habe nicht die Berechtigung, diese Rolle zuzuweisen.", ephemeral=True
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
        target_channel = discord.utils.get(guild.channels, id=1314112301162430464)


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
        target_channel = discord.utils.get(guild.channels, id=1314112392594194482)

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
        channel = interaction.guild.get_channel(1314117160465076264)

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
    
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1316082550493548614/1321534361933316106/093e98cf90f519920d4569e9d0b69d33813821d55aab1a92b434752e2b5c33f4.png?ex=676d9648&is=676c44c8&hm=1688ebeab6de4bde4f5476cdc4f0392e8cb3929dac58e831584a4ee6a88cac71&=&format=webp&quality=lossless&width=1361&height=1361")

    # Nachricht mit Buttons senden
    await interaction.channel.send(embed=embed, view=VerificationButtons())
    await interaction.response.send_message("Verifizierung wurde eingerichtet!", ephemeral=True)

# Slash Command zum Hinzufügen eines Nutzers zu einem Thread
@app_commands.command(name="ticket-add", description="Fügt einen Benutzer zu einem Thread hinzu.")
async def ticket_add(interaction: discord.Interaction, user: discord.Member):  # Ändere den Typ zu str
    # Berechtigungen prüfen
    allowed_roles = ["Owner", "Admin+", "Admin", "Admina", "Server Architekt", "Mod"]
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