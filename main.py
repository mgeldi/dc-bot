import discord
from dotenv import load_dotenv
import os

load_dotenv()

# Intents aktivieren
intents = discord.Intents.default()
intents.guilds = True  # Für Guild-Informationen
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

# Globale Definition von ALLOWED_ROLES
SCHWESTER_ROLE = "Schwester"
BRUDER_ROLE = "Bruder"
ALLOWED_SCHWESTER_ROLES = ["Owner", "Admin+", "Admin", "Admina"]
ALLOWED_BRUDER_ROLES = ["Owner", "Admin+", "Admin"]
roles_to_remove = ["Unverifiziert", "Unverifiziert M", "Unverifiziert W"]
AGE_ROLES = ["15-20", "21-25", "25-30", "30-35", "36-40", "40+"]
CITY_ROLES = [
    "Thüringen", "Schleswig-Holstein", "Sachsen-Anhalt", "Sachsen", "Saarland",
    "Rheinland-Pfalz", "Nordrhein-Westfalen", "Niedersachsen",
    "Mecklenburg-Vorpommern", "Hessen", "Hamburg", "Bremen", "Berlin",
    "Bayern", "Baden-Württemberg", "Burgenland", "Tirol", "Steiermark",
    "Oberösterreich", "Niederösterreich", "Waadt", "Aargau", "Zürich", "Bern",
    "Graubünden"
]
SCHOOL_ROLES = ["Hanafi", "Maliki", "Shafi'i", "Hanbali"]
persistent_views = []  # Liste zum Speichern von Views für die Persistenz


# Hilfsfunktion zum Entfernen anderer Rollen
async def remove_roles_in_category(user, category_roles, guild):
    roles_to_remove = [
        role for role in user.roles if role.name in category_roles
    ]
    if roles_to_remove:
        await user.remove_roles(*roles_to_remove)

def update_dropdown_options(selected_value, options):
    """
    Aktualisiert die Dropdown-Optionen, sodass nur die ausgewählte Option als 'ausgewählt' markiert wird.
    """
    for option in options:
        option.default = (option.value == selected_value)
    return options


# Dropdown-Menü für Altersgruppen
class AgeDropdown(discord.ui.Select):

    def __init__(self):
        options = [
            discord.SelectOption(label="15-20", value="15-20"),
            discord.SelectOption(label="21-25", value="21-25"),
            discord.SelectOption(label="25-30", value="25-30"),
            discord.SelectOption(label="30-35", value="30-35"),
            discord.SelectOption(label="36-40", value="36-40"),
            discord.SelectOption(label="40+", value="40+"),
        ]
        super().__init__(placeholder="Wähle deine Altersgruppe aus",
                         min_values=0,  # Abwählbar
                         max_values=1,
                         options=options,
                         custom_id="age_dropdown")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_roles = interaction.user.roles

        # Rollen, die durch das Dropdown repräsentiert werden
        valid_roles = [discord.utils.get(guild.roles, name=option.value) for option in self.options]
        valid_roles = [role for role in valid_roles if role is not None]  # Nur existierende Rollen

        # Rollen, die der Benutzer derzeit hat und in diesem Dropdown enthalten sind
        current_roles = set(role for role in user_roles if role in valid_roles)

        # Rollen, die in der aktuellen Auswahl sind
        selected_roles = set(discord.utils.get(guild.roles, name=value) for value in self.values)

        # Rollen, die hinzugefügt oder entfernt werden sollen
        roles_to_add = selected_roles - current_roles
        roles_to_remove = current_roles - selected_roles

        # Änderungen anwenden
        if roles_to_add:
            await interaction.user.add_roles(*roles_to_add)
        if roles_to_remove:
            await interaction.user.remove_roles(*roles_to_remove)

        # Nachricht für den Benutzer
        added_roles = ", ".join([role.name for role in roles_to_add])
        removed_roles = ", ".join([role.name for role in roles_to_remove])

        response_message = "Deine Rollen wurden aktualisiert:\n"
        if roles_to_add:
            response_message += f"✅ Hinzugefügt: {added_roles}\n"
        if roles_to_remove:
            response_message += f"❌ Entfernt: {removed_roles}\n"

        if not roles_to_add and not roles_to_remove:
            response_message = "Keine Änderungen vorgenommen."

        await interaction.response.send_message(response_message, ephemeral=True)


class AgeDropdownView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(AgeDropdown())


# Dropdown-Menü für Städte
class CityDropdown(discord.ui.Select):

    def __init__(self):
        options = [
            # Deutschland 🇩🇪
            discord.SelectOption(label="Baden-Württemberg", value="Baden-Württemberg", emoji="🇩🇪"),
            discord.SelectOption(label="Bayern", value="Bayern", emoji="🇩🇪"),
            discord.SelectOption(label="Berlin", value="Berlin", emoji="🇩🇪"),
            discord.SelectOption(label="Bremen", value="Bremen", emoji="🇩🇪"),
            discord.SelectOption(label="Hamburg", value="Hamburg", emoji="🇩🇪"),
            discord.SelectOption(label="Hessen", value="Hessen", emoji="🇩🇪"),
            discord.SelectOption(label="Mecklenburg-Vorpommern", value="Mecklenburg-Vorpommern", emoji="🇩🇪"),
            discord.SelectOption(label="Niedersachsen", value="Niedersachsen", emoji="🇩🇪"),
            discord.SelectOption(label="Nordrhein-Westfalen", value="Nordrhein-Westfalen", emoji="🇩🇪"),
            discord.SelectOption(label="Rheinland-Pfalz", value="Rheinland-Pfalz", emoji="🇩🇪"),
            discord.SelectOption(label="Saarland", value="Saarland", emoji="🇩🇪"),
            discord.SelectOption(label="Sachsen", value="Sachsen", emoji="🇩🇪"),
            discord.SelectOption(label="Sachsen-Anhalt", value="Sachsen-Anhalt", emoji="🇩🇪"),
            discord.SelectOption(label="Schleswig-Holstein", value="Schleswig-Holstein", emoji="🇩🇪"),
            discord.SelectOption(label="Thüringen", value="Thüringen", emoji="🇩🇪"),

            # Österreich 🇦🇹
            discord.SelectOption(label="Burgenland", value="Burgenland", emoji="🇦🇹"),
            discord.SelectOption(label="Linz", value="Linz", emoji="🇦🇹"),
            discord.SelectOption(label="Niederösterreich", value="Niederösterreich", emoji="🇦🇹"),
            discord.SelectOption(label="Oberösterreich", value="Oberösterreich", emoji="🇦🇹"),
            discord.SelectOption(label="Steiermark", value="Steiermark", emoji="🇦🇹"),
            discord.SelectOption(label="Tirol", value="Tirol", emoji="🇦🇹"),
            discord.SelectOption(label="Wien", value="Wien", emoji="🇦🇹"),

            # Schweiz 🇨🇭
            discord.SelectOption(label="Aargau", value="Aargau", emoji="🇨🇭"),
            discord.SelectOption(label="Bern", value="Bern", emoji="🇨🇭"),
            discord.SelectOption(label="Zürich", value="Zürich", emoji="🇨🇭"),
        ]

        super().__init__(placeholder="Wähle deine Stadt aus",
                         min_values=0,  # Abwählbar
                         max_values=1,
                         options=options,
                         custom_id="city_dropdown")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_roles = interaction.user.roles

        # Rollen, die durch das Dropdown repräsentiert werden
        valid_roles = [discord.utils.get(guild.roles, name=option.value) for option in self.options]
        valid_roles = [role for role in valid_roles if role is not None]  # Nur existierende Rollen

        # Rollen, die der Benutzer derzeit hat und in diesem Dropdown enthalten sind
        current_roles = set(role for role in user_roles if role in valid_roles)

        # Rollen, die in der aktuellen Auswahl sind
        selected_roles = set(discord.utils.get(guild.roles, name=value) for value in self.values)

        # Rollen, die hinzugefügt oder entfernt werden sollen
        roles_to_add = selected_roles - current_roles
        roles_to_remove = current_roles - selected_roles

        # Änderungen anwenden
        if roles_to_add:
            await interaction.user.add_roles(*roles_to_add)
        if roles_to_remove:
            await interaction.user.remove_roles(*roles_to_remove)

        # Nachricht für den Benutzer
        added_roles = ", ".join([role.name for role in roles_to_add])
        removed_roles = ", ".join([role.name for role in roles_to_remove])

        response_message = "Deine Rollen wurden aktualisiert:\n"
        if roles_to_add:
            response_message += f"✅ Hinzugefügt: {added_roles}\n"
        if roles_to_remove:
            response_message += f"❌ Entfernt: {removed_roles}\n"

        if not roles_to_add and not roles_to_remove:
            response_message = "Keine Änderungen vorgenommen."

        await interaction.response.send_message(response_message, ephemeral=True)


class CityDropdownView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(CityDropdown())

# Dropdown-Menü für Rechtsschulen
class SchoolDropdown(discord.ui.Select):

    def __init__(self):
        # Mapping der Rollen zu Emojis
        school_emojis = {
            "Hanafi": "📕",
            "Maliki": "📙",
            "Shafi'i": "📗",
            "Hanbali": "📘",
        }

        # Optionen mit Emojis erstellen
        options = [
            discord.SelectOption(
                label=school,
                value=school,
                emoji=school_emojis.get(school, "📖")  # Standard-Emoji, falls keine Zuordnung existiert
            ) for school in SCHOOL_ROLES
        ]

        super().__init__(placeholder="Wähle deine Rechtsschule aus",
                         min_values=0,
                         max_values=1,
                         options=options,
                         custom_id="school_dropdown")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_roles = interaction.user.roles

        # Überprüfen, ob die Rolle existiert
        selected_role_name = self.values[0] if self.values else None
        selected_role = discord.utils.get(guild.roles, name=selected_role_name)

        # Entfernen anderer Schul-Rollen
        school_roles = [
            discord.utils.get(guild.roles, name=school) for school in SCHOOL_ROLES
        ]
        school_roles = [role for role in school_roles if role is not None]

        for role in school_roles:
            if role in user_roles:
                await interaction.user.remove_roles(role)

        # Hinzufügen der ausgewählten Rolle, falls eine gewählt wurde
        if selected_role:
            await interaction.user.add_roles(selected_role)

        response_message = (
            f"Du hast die Rolle **{selected_role_name}** erhalten." 
            if selected_role_name else 
            "Alle Rechtsschulen-Rollen wurden entfernt."
        )

        await interaction.response.send_message(response_message, ephemeral=True)


class SchoolDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(SchoolDropdown())


# Dropdown-Menü für Bildungsrollen
class BildungsrollenDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Quran", value="Quran", emoji="🕋"),
            discord.SelectOption(label="Unterrichte", value="Unterrichte", emoji="🖋️"),
            discord.SelectOption(label="Buchvorlesungen", value="Buchvorlesungen", emoji="📖"),
            discord.SelectOption(label="Vorträge", value="Vorträge", emoji="📚"),
            discord.SelectOption(label="Podcasts", value="Podcasts", emoji="🎙️"),
        ]
        super().__init__(placeholder="Wähle deine Bildungsrollen aus",
                         min_values=0,
                         max_values=len(options),
                         options=options,
                         custom_id="bildungsrollen_dropdown")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_roles = interaction.user.roles

        # Rollen, die durch das Dropdown repräsentiert werden
        valid_roles = [discord.utils.get(guild.roles, name=option.value) for option in self.options]
        valid_roles = [role for role in valid_roles if role is not None]  # Nur existierende Rollen

        # Rollen, die der Benutzer derzeit hat und in diesem Dropdown enthalten sind
        current_roles = set(role for role in user_roles if role in valid_roles)

        # Rollen, die in der aktuellen Auswahl sind
        selected_roles = set(
            discord.utils.get(guild.roles, name=value) for value in self.values if value
        )

        # Rollen, die hinzugefügt oder entfernt werden sollen
        roles_to_add = selected_roles - current_roles
        roles_to_remove = current_roles - selected_roles

        # Änderungen anwenden
        if roles_to_add:
            await interaction.user.add_roles(*roles_to_add)
        if roles_to_remove:
            await interaction.user.remove_roles(*roles_to_remove)

        # Nachricht für den Benutzer
        added_roles = ", ".join([role.name for role in roles_to_add])
        removed_roles = ", ".join([role.name for role in roles_to_remove])

        response_message = "Deine Rollen wurden aktualisiert:\n"
        if roles_to_add:
            response_message += f"✅ Hinzugefügt: {added_roles}\n"
        if roles_to_remove:
            response_message += f"❌ Entfernt: {removed_roles}\n"

        if not roles_to_add and not roles_to_remove:
            response_message = "Keine Änderungen vorgenommen."

        await interaction.response.send_message(response_message, ephemeral=True)


class BildungsrollenDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(BildungsrollenDropdown())


# Slash Command zum Posten der Dropdown-Menüs
@tree.command(name="setup_roles",
              description="Postet die Dropdown-Menüs für die Rollenwahl")
async def setup_roles(interaction: discord.Interaction):
    await interaction.response.send_message("Erstelle Rollen-Auswahl...")

    # Altersgruppen
    embed_age = discord.Embed(title="👥 Wähle deine Altersgruppe",
                              color=discord.Color.blue())
    embed_age.set_image(
        url=
        "https://media.discordapp.net/attachments/1316082550493548614/1320532982422835272/image-5.png?ex=676bebed&is=676a9a6d&hm=c3c3f21935d4969517c71d492272aa1619b0e2ec5e9c6c2b0f92f397bb6108fe&=&format=webp&quality=lossless&width=1440&height=808"
    )  # Thumbnail hinzufügen
    await interaction.channel.send(embed=embed_age, view=AgeDropdownView())

    # Städte
    embed_city = discord.Embed(
        title="🌆 Wähle dein Bundesland oder deine Stadt",
        color=discord.Color.green())
    embed_city.set_image(
        url=
        "https://media.discordapp.net/attachments/1316082550493548614/1320475707343896606/image.png?ex=676bb695&is=676a6515&hm=c19f2d2cfc26ea64014cb033af0d063f4c123169671da7d057b5ca5ffab6d49a&=&format=webp&quality=lossless&width=1440&height=810"
    )
    await interaction.channel.send(embed=embed_city, view=CityDropdownView())

    # Rechtsschulen
    embed_school = discord.Embed(title="📚 Wähle deine Rechtsschule",
                                 color=discord.Color.gold())
    embed_school.set_image(
        url=
        "https://media.discordapp.net/attachments/1316082550493548614/1320532983148580864/image-4.png?ex=676bebed&is=676a9a6d&hm=0c614303d4812668315d296090abd00f8953721dc88420c1ad483057fb28be23&=&format=webp&quality=lossless&width=1440&height=808"
    )
    await interaction.channel.send(embed=embed_school,
                                   view=SchoolDropdownView())

    # Bildungsrollen
    embed_school = discord.Embed(title="📖 Wähle deine islamischen Bildungsrollen",
                                 color=discord.Color.red())
    embed_school.set_image(
        url=
        "https://media.discordapp.net/attachments/1316082550493548614/1321257663987716156/image.png?ex=676d3d56&is=676bebd6&hm=f0963f170dd25231a2ca725c3d87cd9481870d8c42522f4a07c5024ea9af5e15&=&format=webp&quality=lossless&width=1443&height=813"
    )
    await interaction.channel.send(embed=embed_school,
                                   view=BildungsrollenDropdownView())


SCHWESTER_ROLE = "Schwester"
BRUDER_ROLE = "Bruder"
ALLOWED_SCHWESTER_ROLES = ["Owner", "Admin+", "Admin", "Admina"]
ALLOWED_BRUDER_ROLES = ["Owner", "Admin+", "Admin"]

# Slash-Command: verify-schwester
@tree.command(name="verify-schwester", 
              description="Weist einem Benutzer die Rolle 'Schwester' zu.")
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
@tree.command(name="verify-bruder", 
              description="Weist einem Benutzer die Rolle 'Bruder' zu.")
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

# Slash Command zum Hinzufügen eines Nutzers zu einem Thread
@tree.command(name="ticket-add", description="Fügt einen Benutzer zu einem Thread hinzu.")
async def ticket_add(interaction: discord.Interaction, user: discord.Member):  # Ändere den Typ zu str
    # Berechtigungen prüfen
    allowed_roles = ["Owner", "Admin", "Mod"]
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
@tree.command(name="setup_verification", description="Richtet die Verifizierung mit Buttons ein.")
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

@bot.tree.command(name="sheikh-info")
async def sheikh_info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Sheikh Dr. Adnan Yusuf Husain",
        description="Hier einige Informationen über den Sheikh:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Erfahrung & Bildung",
        value=(
            "• 20 Jahre Erfahrung im Erlernen und Lehren von Arabisch als Fremdsprache.\n"
            "• Bachelor, Master und Doktorat an renommierten arabischen Universitäten.\n"
            "• Doktor in Tafsir.\n"
        ),
        inline=False
    )

    embed.add_field(
        name="Zukünftige Aktivitäten",
        value=(
            "• Der Sheikh wird voraussichtlich ab Mitte Januar 2025 regelmäßig auf diesem Server aktiv sein.\n"
            "• Geplant sind tiefgehende Vorträge zu verschiedenen islamischen Themengebieten."
        ),
        inline=False
    )

    embed.add_field(
        name="Relevante Links",
        value=(
            "[Website des Sheikh mit kostenlosen Kursen](https://www.islamwissenschaften.com/)\n"
            "[Arabisch Kurs auf Skool mit individuellem Lehrplan](https://www.skool.com/lerne-arabisch/about)\n"
            "[Telegram Gruppe des Sheikh](https://t.me/adnanyh)"
        ),
        inline=False
    )

    embed.set_footer(text="Wir freuen uns, den Sheikh auf unserem Server begrüßen zu dürfen!")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="sheikh-kurse")
async def sheikh_kurse(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Sheikh Dr. Adnan Yusuf Husain - Kurse",
        description="Hier findest du eine Übersicht über die Kurse, die vom Sheikh angeboten werden:",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Kostenlose Kurse - islamwissenschaften.com",
        value=(
            "• Alle Kurse sind kostenlos und beinhalten folgende Themen:\n"
            "  • Aqidah\n"
            "  • Arabisch (Grammatik)\n"
            "  • Fiqh\n"
            "  • Qur'anwissenschaften\n"
            "  • Tafsir\n"
            "  • Usul al-Fiqh\n"
            "• Kursplattform: [Islamwissenschaften.com](https://www.islamwissenschaften.com/courses)"
        ),
        inline=False
    )

    embed.add_field(
        name="Kostenpflichtiger Arabisch-Kurs",
        value=(
            "• Der Sheikh bietet auch einen Arabisch-Kurs an, der auf deinen individuellen Lernplan abgestimmt wird.\n"
            "• Der Kurs ist für alle Lernstufen geeignet und bietet ein personalisiertes Lernerlebnis.\n"
            "• Weitere Informationen findest du hier: [Skool Arabisch-Kurs](https://www.skool.com/lerne-arabisch/about)"
        ),
        inline=False
    )

    embed.add_field(
        name="Warum diese Kurse?",
        value=(
            "• Alle Kurse werden auf Deutsch angeboten.\n"
            "• Du erhältst eine fundierte und strukturierte Ausbildung in den Bereichen Islam und Arabisch.\n"
            "• Der Sheikh hat jahrzehntelange Erfahrung und vermittelt authentisches Wissen gemäß der Ahlus Sunnah wal Jamaah.\n"
            "• Die kostenlose Kursplattform bietet dir Zugang zu einer Vielzahl von Themen, um dein Wissen zu erweitern."
        ),
        inline=False
    )

    embed.set_footer(text="Nutze die Gelegenheit, dein Wissen zu erweitern und in die islamischen Wissenschaften einzutauchen!")

    await interaction.response.send_message(embed=embed)


# Bot starten
@bot.event
async def on_ready():
    await tree.sync()  # Slash Commands mit Discord synchronisieren
    bot.add_view(AgeDropdownView())
    bot.add_view(CityDropdownView())
    bot.add_view(SchoolDropdownView())
    bot.add_view(VerificationButtons())
    print(f"Bot ist online! Eingeloggt als {bot.user}")


bot.run(os.getenv("BOT_TOKEN"))

