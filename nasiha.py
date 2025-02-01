import discord
from discord import app_commands

CATEGORY_ID = 1335398485091942550  # ID der Nasiha-Kategorie
ALLOWED_ROLES = ["Owner", "Admin+", "Admin", "Admina", "Server Architekt", "Mod", "Supporter"]


def user_has_allowed_role(interaction: discord.Interaction) -> bool:
    """Prüft, ob der Benutzer eine der erlaubten Rollen hat."""
    user_roles = [role.name for role in interaction.user.roles]
    return any(role in ALLOWED_ROLES for role in user_roles)

# Slash-Command: nasiha
@app_commands.command(name="nasiha", description="Erstellt einen Nasiha-Channel für einen Nutzer.")
async def nasiha(interaction: discord.Interaction, user: discord.Member):
    # Berechtigungen prüfen
    if not user_has_allowed_role(interaction):
        await interaction.response.send_message(
            "Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True
        )
        return

    guild = interaction.guild

    # Kategorie holen
    category = discord.utils.get(guild.categories, id=CATEGORY_ID)
    if not category:
        await interaction.response.send_message(
            "Die Nasiha-Kategorie existiert nicht oder die ID ist ungültig.", ephemeral=True
        )
        return

    # Überprüfen, ob ein Channel für den Nutzer bereits existiert
    existing_channel = discord.utils.get(category.channels, name=user.name.lower())
    if existing_channel:
        await interaction.response.send_message(
            f"Ein Nasiha-Channel für {user.mention} existiert bereits: {existing_channel.mention}", ephemeral=True
        )
        return

    # Channel erstellen
    try:
        nasiha_channel = await guild.create_text_channel(
            name=user.name.lower(),
            category=category,
            topic=f"Nasiha für {user.name}",
        )

        # Berechtigungen setzen
        await nasiha_channel.set_permissions(user, read_messages=True, send_messages=True, read_message_history=True)
        await nasiha_channel.set_permissions(interaction.guild.default_role, read_messages=False)

        # Nachricht senden
        await nasiha_channel.send(
            content=(
                f"{user.mention}\n\n"
                "As-salamu alaikum wa rahmatullahi wa barakatuh,\n\n"
                "ein Teammitglied wird sich in Kürze bei dir melden. "
                "Bitte gedulde dich, bis das Teammitglied die Situation geschildert hat."
            )
        )

        # Bestätigung für den ausführenden Benutzer
        await interaction.response.send_message(
            f"Der Nasiha-Channel {nasiha_channel.mention} wurde erfolgreich für {user.mention} erstellt.", ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            f"Ein Fehler ist aufgetreten: {e}", ephemeral=True
        )

# Slash-Command: nasiha-close
@app_commands.command(name="nasiha-close", description="Schließt den aktuellen Nasiha-Channel.")
async def nasiha_close(interaction: discord.Interaction):
    # Berechtigungen prüfen
    if not user_has_allowed_role(interaction):
        await interaction.response.send_message(
            "Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True
        )
        return

    channel = interaction.channel

    # Überprüfen, ob der Channel in der Nasiha-Kategorie ist
    if channel.category_id != CATEGORY_ID:
        await interaction.response.send_message(
            "Dieser Befehl kann nur in einem Nasiha-Channel ausgeführt werden.", ephemeral=True
        )
        return

    # Channel löschen
    try:
        await channel.delete(reason=f"Nasiha-Channel wurde von {interaction.user} geschlossen.")
    except discord.Forbidden:
        await interaction.response.send_message(
            "Ich habe keine Berechtigung, diesen Channel zu löschen.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"Ein Fehler ist aufgetreten: {e}", ephemeral=True
        )