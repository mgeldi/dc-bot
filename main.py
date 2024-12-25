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
BRUDER_ROLES = ["Bruder", "Bruder+"]
SCHWESTER_ROLES = ["Schwester", "Schwester+"]
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
SCHOOL_ROLES = ["Hanbali", "Shafi'i", "Maliki", "Hanafi"]
persistent_views = []  # Liste zum Speichern von Views für die Persistenz


# Hilfsfunktion zum Entfernen anderer Rollen
async def remove_roles_in_category(user, category_roles, guild):
    roles_to_remove = [
        role for role in user.roles if role.name in category_roles
    ]
    if roles_to_remove:
        await user.remove_roles(*roles_to_remove)


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
                         min_values=1,
                         max_values=1,
                         options=options,
                         custom_id="age_dropdown")

    async def callback(self, interaction: discord.Interaction):
        selected_role_name = self.values[0]
        guild = interaction.guild

        # Überprüfen, ob die Rolle existiert
        selected_role = discord.utils.get(guild.roles, name=selected_role_name)
        if selected_role is None:
            await interaction.response.send_message(
                f"Die Rolle **{selected_role_name}** existiert nicht.",
                ephemeral=True)
            return

        # Entfernen anderer Altersrollen und Hinzufügen der neuen Rolle
        await remove_roles_in_category(interaction.user, AGE_ROLES, guild)
        await interaction.user.add_roles(selected_role)
        await interaction.response.send_message(
            f"Du hast die Rolle **{selected_role_name}** erhalten. Andere Altersrollen wurden entfernt.",
            ephemeral=True)


class AgeDropdownView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(AgeDropdown())


# Dropdown-Menü für Städte
class CityDropdown(discord.ui.Select):

    def __init__(self):
        options = [
            # Deutschland 🇩🇪
            discord.SelectOption(label="Thüringen",
                                 value="Thüringen",
                                 emoji="🇩🇪"),
            discord.SelectOption(label="Schleswig-Holstein",
                                 value="Schleswig-Holstein",
                                 emoji="🇩🇪"),
            discord.SelectOption(label="Sachsen-Anhalt",
                                 value="Sachsen-Anhalt",
                                 emoji="🇩🇪"),
            discord.SelectOption(label="Sachsen", value="Sachsen", emoji="🇩🇪"),
            discord.SelectOption(label="Saarland",
                                 value="Saarland",
                                 emoji="🇩🇪"),
            discord.SelectOption(label="Rheinland-Pfalz",
                                 value="Rheinland-Pfalz",
                                 emoji="🇩🇪"),
            discord.SelectOption(label="Nordrhein-Westfalen",
                                 value="Nordrhein-Westfalen",
                                 emoji="🇩🇪"),
            discord.SelectOption(label="Niedersachsen",
                                 value="Niedersachsen",
                                 emoji="🇩🇪"),
            discord.SelectOption(label="Mecklenburg-Vorpommern",
                                 value="Mecklenburg-Vorpommern",
                                 emoji="🇩🇪"),
            discord.SelectOption(label="Hessen", value="Hessen", emoji="🇩🇪"),
            discord.SelectOption(label="Hamburg", value="Hamburg", emoji="🇩🇪"),
            discord.SelectOption(label="Bremen", value="Bremen", emoji="🇩🇪"),
            discord.SelectOption(label="Berlin", value="Berlin", emoji="🇩🇪"),
            discord.SelectOption(label="Bayern", value="Bayern", emoji="🇩🇪"),
            discord.SelectOption(label="Baden-Württemberg",
                                 value="Baden-Württemberg",
                                 emoji="🇩🇪"),

            # Österreich 🇦🇹
            discord.SelectOption(label="Burgenland",
                                 value="Burgenland",
                                 emoji="🇦🇹"),
            discord.SelectOption(label="Tirol", value="Tirol", emoji="🇦🇹"),
            discord.SelectOption(label="Steiermark",
                                 value="Steiermark",
                                 emoji="🇦🇹"),
            discord.SelectOption(label="Oberösterreich",
                                 value="Oberösterreich",
                                 emoji="🇦🇹"),
            discord.SelectOption(label="Niederösterreich",
                                 value="Niederösterreich",
                                 emoji="🇦🇹"),

            # Schweiz 🇨🇭
            discord.SelectOption(label="Waadt", value="Waadt", emoji="🇨🇭"),
            discord.SelectOption(label="Aargau", value="Aargau", emoji="🇨🇭"),
            discord.SelectOption(label="Zürich", value="Zürich", emoji="🇨🇭"),
            discord.SelectOption(label="Bern", value="Bern", emoji="🇨🇭"),
            discord.SelectOption(label="Graubünden",
                                 value="Graubünden",
                                 emoji="🇨🇭"),
        ]
        super().__init__(placeholder="Wähle deine Stadt aus",
                         min_values=1,
                         max_values=1,
                         options=options,
                         custom_id="city_dropdown")

    async def callback(self, interaction: discord.Interaction):
        selected_role_name = self.values[0]
        guild = interaction.guild

        # Überprüfen, ob die Rolle existiert
        selected_role = discord.utils.get(guild.roles, name=selected_role_name)
        if selected_role is None:
            await interaction.response.send_message(
                f"Die Rolle **{selected_role_name}** existiert nicht.",
                ephemeral=True)
            return

        # Entfernen anderer Städte-Rollen und Hinzufügen der neuen Rolle
        await remove_roles_in_category(interaction.user, CITY_ROLES, guild)
        await interaction.user.add_roles(selected_role)
        await interaction.response.send_message(
            f"Du hast die Rolle **{selected_role_name}** erhalten. Andere Städte-Rollen wurden entfernt.",
            ephemeral=True)


class CityDropdownView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(CityDropdown())


# Dropdown-Menü für Rechtsschulen
class SchoolDropdown(discord.ui.Select):

    def __init__(self):
        options = [
            discord.SelectOption(label=school, value=school)
            for school in SCHOOL_ROLES
        ]
        super().__init__(placeholder="Wähle deine Rechtsschule aus",
                         min_values=1,
                         max_values=1,
                         options=options,
                         custom_id="school_dropdown")

    async def callback(self, interaction: discord.Interaction):
        selected_role_name = self.values[0]
        guild = interaction.guild

        # Überprüfen, ob die Rolle existiert
        selected_role = discord.utils.get(guild.roles, name=selected_role_name)
        if selected_role is None:
            await interaction.response.send_message(
                f"Die Rolle **{selected_role_name}** existiert nicht.",
                ephemeral=True)
            return

        # Entfernen anderer Schul-Rollen und Hinzufügen der neuen Rolle
        await remove_roles_in_category(interaction.user, SCHOOL_ROLES, guild)
        await interaction.user.add_roles(selected_role)
        await interaction.response.send_message(
            f"Du hast die Rolle **{selected_role_name}** erhalten. Andere Rechtsschulen-Rollen wurden entfernt.",
            ephemeral=True)


class SchoolDropdownView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(SchoolDropdown())


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
                                 color=discord.Color.purple())
    embed_school.set_image(
        url=
        "https://media.discordapp.net/attachments/1316082550493548614/1320532983148580864/image-4.png?ex=676bebed&is=676a9a6d&hm=0c614303d4812668315d296090abd00f8953721dc88420c1ad483057fb28be23&=&format=webp&quality=lossless&width=1440&height=808"
    )
    await interaction.channel.send(embed=embed_school,
                                   view=SchoolDropdownView())

# Dropdown-Menü für Städte
# class BildungsrollenDropdown(discord.ui.Select):

#     def __init__(self):
#         options = [
#             discord.SelectOption(label="Quran",
#                                  value="Quran",
#                                  emoji="🕋"),
#             discord.SelectOption(label="Unterrichte",
#                                  value="Unterrichte",
#                                  emoji="🖋️"),
#             discord.SelectOption(label="Buchvorlesungen",
#                                  value="Buchvorlesungen",
#                                  emoji="📖"),
#             discord.SelectOption(label="Vorträge",
#                                  value="Vorträge",
#                                  emoji="📚"),
#             discord.SelectOption(label="Podcasts",
#                                  value="Podcasts",
#                                  emoji="🎙️"),
#         ]
#         super().__init__(placeholder="Wähle deine Bildungsrollen aus",
#                          min_values=1,
#                          max_values=1,
#                          options=options,
#                          custom_id="bildungsrollen_dropdown")

#     async def callback(self, interaction: discord.Interaction):
#         selected_role_name = self.values[0]
#         guild = interaction.guild

#         # Überprüfen, ob die Rolle existiert
#         selected_role = discord.utils.get(guild.roles, name=selected_role_name)
#         if selected_role is None:
#             await interaction.response.send_message(
#                 f"Die Rolle **{selected_role_name}** existiert nicht.",
#                 ephemeral=True)
#             return

#         # Entfernen anderer Städte-Rollen und Hinzufügen der neuen Rolle
#         await remove_roles_in_category(interaction.user, CITY_ROLES, guild)
#         await interaction.user.add_roles(selected_role)
#         await interaction.response.send_message(
#             f"Du hast die Rolle **{selected_role_name}** erhalten. Andere Städte-Rollen wurden entfernt.",
#             ephemeral=True)


# Slash Command definieren
@tree.command(name="verifizieren",
              description="Weist einem Benutzer eine bestimmte Rolle zu.")
async def verifizieren(
        interaction: discord.Interaction,
        user: discord.Member,  # Benutzer auswählen
        role: str  # Rolle auswählen
):
    # Berechtigung des ausführenden Benutzers prüfen
    executor_roles = [r.name for r in interaction.user.roles]
    if any(r.startswith("Verifiziererin")
           for r in executor_roles) and role not in SCHWESTER_ROLES:
        await interaction.response.send_message(
            "Du darfst nur die Rollen 'Schwester' oder 'Schwester+' zuweisen.",
            ephemeral=True)
        return
    elif any(r.startswith("Verifizierer")
             for r in executor_roles) and role not in BRUDER_ROLES:
        await interaction.response.send_message(
            "Du darfst nur die Rollen 'Bruder' oder 'Bruder+' zuweisen.",
            ephemeral=True)
        return

    # Überprüfen, ob die Rolle auf dem Server existiert
    guild_role = discord.utils.get(interaction.guild.roles, name=role)
    if guild_role is None:
        await interaction.response.send_message(
            f"Die Rolle '{role}' existiert nicht auf diesem Server.",
            ephemeral=True)
        return

    # Zuweisung der Rolle
    try:
        await user.add_roles(guild_role)

        # Entfernen der Rolle "Unverifiziert" sowie "Unverifiziert M|W"
        for role_name in roles_to_remove:
            role_to_remove = discord.utils.get(interaction.guild.roles, name=role_name)
            if role_to_remove and role_to_remove in user.roles:
                await user.remove_roles(role_to_remove)

        await interaction.response.send_message(
            f"Die Rolle '{role}' wurde erfolgreich {user.mention} zugewiesen!")
    except discord.Forbidden:
        await interaction.response.send_message(
            "Ich habe nicht die Berechtigung, diese Rolle zuzuweisen.",
            ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(
            f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)


# Autocomplete für den `role`-Parameter
@verifizieren.autocomplete("role")
async def role_autocomplete(interaction: discord.Interaction, current: str):
    # Berechtigung des ausführenden Benutzers prüfen
    executor_roles = [r.name for r in interaction.user.roles]

    if any(r.startswith("Verifiziererin") for r in executor_roles):
        allowed_roles = SCHWESTER_ROLES
    elif any(r.startswith("Verifizierer") for r in executor_roles):
        allowed_roles = BRUDER_ROLES
    else:
        allowed_roles = [
        ]  # Keine Rollen anzeigen, falls keine Berechtigung vorhanden ist

    # Nur erlaubte Rollen anzeigen, die zur Eingabe passen
    matching_roles = [
        role for role in allowed_roles if current.lower() in role.lower()
    ]
    return [
        discord.app_commands.Choice(name=role, value=role)
        for role in matching_roles
    ]

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

    @discord.ui.button(label="♂️Muslim", style=discord.ButtonStyle.blurple, custom_id="muslim_button")
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

    @discord.ui.button(label="♀️Muslima", style=discord.ButtonStyle.red, custom_id="muslima_button")
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

    @discord.ui.button(label="Ich habe Interesse am Islam", style=discord.ButtonStyle.green, custom_id="interest_button")
    async def interest_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_unverifiziert = discord.utils.get(interaction.guild.roles, name="Unverifiziert")
        role_interessiert = discord.utils.get(interaction.guild.roles, name="Interessiert")
        category = interaction.guild.get_channel(1314116985499553812)  # Kategorie-ID für Interessierte
        role_sonstige = discord.utils.get(interaction.guild.roles, name="Sonstige")

        if role_unverifiziert in interaction.user.roles:
            await interaction.user.add_roles(role_interessiert)
            await interaction.user.remove_roles(role_unverifiziert)

            # Erstellen eines neuen Channels
            new_channel = await category.create_text_channel(
                name=f"dawah-{interaction.user.name}",
                overwrites={
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    role_sonstige: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    discord.utils.get(interaction.guild.roles, name="Owner"): discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    discord.utils.get(interaction.guild.roles, name="Admin"): discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
            )

            # Begrüßungsnachricht
            await new_channel.send(
                f"""Willkommen {interaction.user.mention},

unsere Ansprechpartner ({role_sonstige.mention}) werden sich bald bei dir melden! 
Wenn du Fragen oder Gedanken hast, kannst du sie gerne hier teilen. 
Wir freuen uns, mit dir ins Gespräch zu kommen!"""
            )

            # Ephemeral-Message zur Bestätigung
            await interaction.response.send_message(
                f"Ein neuer Channel wurde für dich erstellt: {new_channel.mention}. Bitte fahre dort fort.", ephemeral=True
            )

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


# Bot starten
@bot.event
async def on_ready():
    await tree.sync()  # Slash Commands mit Discord synchronisieren
    bot.add_view(AgeDropdownView())
    bot.add_view(CityDropdownView())
    bot.add_view(SchoolDropdownView())
    print(f"Bot ist online! Eingeloggt als {bot.user}")


bot.run(os.getenv("BOT_TOKEN"))

