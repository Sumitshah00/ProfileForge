import os
import json
import requests
import time
from datetime import datetime
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

# Initialize colorama
init(autoreset=True)

# Initialize Rich console
console = Console()

class GitHubProfileGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.console = Console()
        self.version = "1.0.0"
        self.admin_name = "HackSageX (Sumit Shah)"

    def display_banner(self):
        """Display an attractive ASCII banner"""
        banner = f"""
{Fore.CYAN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.CYAN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣞⣥⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.CYAN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡞⢉⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.MAGENTA}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣒⣉⠐⡶⠲⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⡞⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.MAGENTA}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⢶⣄⣈⣳⣄⡀⠀⠀⠀⠀⢠⠧⢾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.MAGENTA}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢷⡀⠑⡄⠀⠀⠀⡏⢀⡾⠀⠀⠀⣀⣤⠤⠤⠤⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.YELLOW}⠀⠀⠀⠀⣠⣴⣎⣉⠐⢶⠦⠤⣀⠀⠀⠀⠀⠀⠀⠀⠹⣦⠼⣆⠀⢰⠓⢺⡇⣠⡴⠋⠁⠀⠀⠀⠀⠀⠙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.YELLOW}⠀⠀⠀⠈⠋⠁⠀⠉⠙⠛⠶⣤⣀⢙⡟⢦⡀⠀⠀⠀⠀⢸⡀⠸⡄⡆⠀⣿⣴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.YELLOW}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣥⣄⡼⠛⢢⡀⠀⠀⢳⣀⣇⣇⢀⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⡙⢢⣀⢸⢋⣉⣿⣽⠁⠀⠀⠀⠀⠀⠀⠀⠀⣠⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣁⣨⠟⠉⠁⠀⠀⢣⡀⠀⠀⠀⠀⠀⣠⣴⣋⠤⠴⡶⠤⠔⠒⠲⣤⣀⠀⠀⠀⠀
{Fore.GREEN}⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠤⢤⡔⠊⠉⠉⠉⣺⠉⡽⠁⠀⠀⠀⠀⠀⠀⠉⡶⢶⡶⠒⠋⣿⣉⣀⣀⡴⠷⠶⠶⠤⠖⠻⢦⣉⣐⣄⠀
{Fore.BLUE}⠀⠀⠀⠀⠀⣠⠴⠒⠋⠉⣧⣤⠴⠓⠒⠒⠒⠛⢙⡿⠀⣤⡀⠀⠀⠀⠀⠀⢀⠽⣶⣗⣚⣉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢧
{Fore.BLUE}⠀⠀⡤⠚⢉⣹⠶⠒⠋⠉⠁⠀⠀⠀⠀⠀⡠⢂⡽⣧⠸⠍⠀⠀⠀⠀⠀⣰⡞⣶⣿⣤⣄⣹⡉⠉⠉⠑⣶⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.BLUE}⢀⣾⡤⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣷⠋⠀⠹⣇⣀⢶⣾⣧⣴⠋⣹⣿⣏⠙⢄⠀⠈⠉⠉⠛⠚⠳⢦⣈⣑⣦⠀⠀⠀⠀⠀⠀⠀
{Fore.WHITE}⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠃⠀⠀⠀⠈⣹⢟⡿⠃⠙⣏⠉⢳⡹⣦⣈⣧⠀⠀⠀⠀⠀⠀⠀⠈⢷⡄⢣⠀⠀⠀⠀⠀⠀
{Fore.WHITE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣾⠿⠋⠀⠀⠀⠹⣆⣠⡇⢻⡇⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⠄⠀⠀⠀⠀⠀
{Fore.WHITE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⣿⠁⢣⢸⣇⣠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀
{Fore.WHITE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣀⣈⡆⣿⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⡟⠀⢸⣧⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⢣⠀⢺⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡧⡼⠀⣾⡖⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⣿⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.CYAN}   {Fore.WHITE}[+] Created by {Fore.GREEN}{self.admin_name}{Fore.WHITE}
{Fore.CYAN}   {Fore.WHITE}[+] {Fore.YELLOW}Generate Awesome GitHub Profile READMEs with Style{Fore.WHITE}
{Fore.CYAN}   {Fore.WHITE}[+] Version: {Fore.GREEN}{self.version}{Fore.WHITE}
        """
        print(banner)

    def animate_loading(self, text):
        """Display an animated loading message"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(text, total=None)
            time.sleep(2)  # Simulate processing time

    def fetch_github_data(self, username):
        """Fetch GitHub user data and repositories with loading animation"""
        try:
            self.animate_loading(f"Fetching data for {username}...")

            # GitHub API endpoints
            user_url = f"https://api.github.com/users/{username}"
            repos_url = f"https://api.github.com/users/{username}/repos"

            # Fetch user data
            user_response = requests.get(user_url)
            user_data = user_response.json()

            if user_response.status_code != 200:
                console.print(f"[bold red]Error fetching user data: {user_data.get('message', 'Unknown error')}[/bold red]")
                return None, None

            # Fetch repositories
            repos_response = requests.get(repos_url)
            repos_data = repos_response.json()

            if repos_response.status_code != 200:
                console.print(f"[bold red]Error fetching repos: {repos_data.get('message', 'Unknown error')}[/bold red]")
                return None, None

            # Fetch contributions
            contributions = self.fetch_contributions(username)

            return user_data, repos_data, contributions

        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            return None, None, None

    def fetch_contributions(self, username):
        """Estimate contributions (simplified as GitHub API doesn't directly provide this)"""
        try:
            # This is a very simplified version - in reality, you'd need web scraping
            # or GitHub's GraphQL API with authentication to get accurate contribution data
            events_url = f"https://api.github.com/users/{username}/events/public"
            response = requests.get(events_url)

            if response.status_code == 200:
                return len(response.json())
            return 0
        except:
            return 0

    def get_language_icons(self, languages):
        """Get icon for programming languages"""
        icons = {
            "Python": "🐍",
            "JavaScript": "🟨",
            "TypeScript": "🔷",
            "Java": "☕",
            "C++": "🔧",
            "C#": "🎮",
            "PHP": "🐘",
            "Ruby": "💎",
            "Go": "🦦",
            "Swift": "🍎",
            "Kotlin": "🤖",
            "Rust": "🦀",
            "HTML": "🌐",
            "CSS": "🎨",
            "Shell": "🐚",
            "Jupyter Notebook": "📓"
        }

        return {lang: icons.get(lang, "📄") for lang in languages}

    def generate_stats_badge(self, text, value, color="blue"):
        """Generate a shield.io badge with value"""
        clean_text = text.replace(' ', '%20')
        clean_value = str(value).replace(' ', '%20')
        return f"![{text}](https://img.shields.io/badge/{clean_text}-{clean_value}-{color}?style=for-the-badge)"

    def generate_readme(self, username, user_data, repos_data, contributions):
        """Generate attractive README.md content with emojis, badges and more details"""
        if not user_data or not repos_data:
            return None

        # Calculate stats
        total_stars = sum(repo['stargazers_count'] for repo in repos_data)
        total_forks = sum(repo['forks_count'] for repo in repos_data)
        languages = {}
        for repo in repos_data:
            if repo['language']:
                languages[repo['language']] = languages.get(repo['language'], 0) + 1

        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:6]
        language_icons = self.get_language_icons(dict(top_languages).keys())

        # Current date for updates
        current_date = datetime.now().strftime("%B %d, %Y")

        # Social links with icons
        social_links = []
        if user_data.get('blog'):
            social_links.append(f"<a href='{user_data['blog']}' target='_blank'><img alt='Website' src='https://img.shields.io/badge/Website-%23FF4500.svg?&style=for-the-badge&logo=rss&logoColor=white' /></a>")

        social_links.append(f"<a href='https://github.com/{username}' target='_blank'><img alt='GitHub' src='https://img.shields.io/badge/github-%23181717.svg?&style=for-the-badge&logo=github&logoColor=white' /></a>")

        if user_data.get('twitter_username'):
            social_links.append(f"<a href='https://twitter.com/{user_data['twitter_username']}' target='_blank'><img alt='Twitter' src='https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white' /></a>")

        # Additional social links
        social_links.append(f"<a href='mailto:example@email.com' target='_blank'><img alt='Email' src='https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white' /></a>")
        social_links.append(f"<a href='https://linkedin.com/in/{username}' target='_blank'><img alt='LinkedIn' src='https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white' /></a>")

        social_links_str = " ".join(social_links)

        # Create README content with banner
        readme_content = f"""
<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/241765440-80728820-e06b-4f96-9c9e-9df46f0cc0a5.gif" alt="Banner" width="100%">
</p>

<h1 align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=30&pause=1000&center=true&vCenter=true&width=600&height=100&lines=Hi+There!+👋;I'm+{user_data['name'] or username};{user_data['bio'] or 'Passionate Developer'}" alt="Typing SVG" />
  </a>
</h1>

<div align="center">

![Profile Views](https://komarev.com/ghpvc/?username={username}&color=blueviolet&style=for-the-badge)

<img src="{user_data['avatar_url']}" width="200" height="200" style="border-radius: 50%;" alt="Profile Picture"/>

<blockquote>
<p><em>"{user_data['bio'] or 'Code is poetry written for both humans and machines.'}"</em></p>
</blockquote>

{social_links_str}

</div>

---

<details open>
<summary><h2>🚀 About Me</h2></summary>

- 🔭 I'm currently working on **{repos_data[0]['name'] if repos_data else 'exciting projects'}**
- 🌱 I'm currently learning **advanced development techniques**
- 👯 I'm looking to collaborate on **open-source projects**
- 💬 Ask me about **{", ".join([lang for lang, _ in top_languages[:3]])}**
- 📫 How to reach me: {user_data['email'] if user_data.get('email') else 'GitHub Messages'}
- 🌍 Location: {user_data['location'] if user_data.get('location') else 'Earth'}
- ⚡ Fun fact: The first computer bug was an actual bug!
</details>

---

<details open>
<summary><h2>📊 GitHub Stats & Activity</h2></summary>

<h3 align="center">🔥 Streak Stats</h3>
<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user={username}&theme=radical&hide_border=true" alt="GitHub Streak" />
</p>

<h3 align="center">💻 GitHub Profile Stats</h3>
<p align="center">
  <img alt="GitHub Stats" src="https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&theme=radical&hide_border=true&count_private=true" />
  <img alt="Top Languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&theme=radical&hide_border=true" />
</p>

<b>Note:</b> Top languages is only a metric of the languages my public code consists of and doesn't reflect experience or skill level.

<h3 align="center">📈 Activity Graph</h3>
<p align="center">
  <img alt="Activity Graph" src="https://github-readme-activity-graph.vercel.app/graph?username={username}&theme=redical&hide_border=true" />
</p>
</details>

---

<details open>
<summary><h2>🛠️ My Tech Stack</h2></summary>
<div align="center">
"""
        # Tech stack - add more badges based on languages
        tech_stack = {
            "Languages": ["JavaScript", "Python", "HTML", "CSS", "TypeScript", "C++", "Java"],
            "Frameworks": ["React", "Node.js", "Express", "Django", "Flask", "TensorFlow"],
            "Databases": ["MongoDB", "MySQL", "PostgreSQL", "SQLite", "Redis"],
            "Tools": ["Git", "GitHub", "VS Code", "Docker", "AWS", "Heroku", "Postman"]
        }

        # Add language badges with icons from the user's repos first
        for lang, count in top_languages:
            icon = language_icons.get(lang, "📄")
            badge_name = lang.replace(' ', '%20').replace('+', '%2B').replace('#', 'Sharp')
            logo_name = self.get_correct_logo_name(lang)
            readme_content += f'<img src="https://img.shields.io/badge/{badge_name}-{self.get_language_color(lang)}?style=for-the-badge&logo={logo_name}&logoColor=white" alt="{lang}" /> '

        # Add other tech stack categories
        for category, techs in tech_stack.items():
            # Only include a few from each category, avoiding duplicates with user's actual languages
            existing_langs = [lang for lang, _ in top_languages]
            remaining_techs = [tech for tech in techs if tech not in existing_langs][:3]

            if remaining_techs:
                readme_content += f"\n\n<h3>{category}</h3>\n"
                for tech in remaining_techs:
                    badge_name = tech.replace(' ', '%20').replace('.', '%2E').replace('+', '%2B').replace('#', 'Sharp')
                    logo_name = tech.lower().replace(' ', '').replace('.', '').replace('+', 'plus').replace('#', 'sharp')

                    # Get the correct logo name for this technology
                    logo_name = self.get_correct_logo_name(tech)

                    readme_content += f'<img src="https://img.shields.io/badge/{badge_name}-{self.get_tech_color(tech)}?style=for-the-badge&logo={logo_name}&logoColor=white" alt="{tech}" /> '

        readme_content += """
</div>
</details>

---

<details open>
<summary><h2>🏆 GitHub Achievements</h2></summary>
<div align="center">
"""
        # Add achievement badges
        readme_content += f"""
![Stars](https://img.shields.io/badge/Stars-{total_stars}-gold?style=for-the-badge&logo=github)
![Repositories](https://img.shields.io/badge/Repos-{user_data['public_repos']}-blue?style=for-the-badge&logo=github)
![Followers](https://img.shields.io/badge/Followers-{user_data['followers']}-blueviolet?style=for-the-badge&logo=github)
![Forks](https://img.shields.io/badge/Forks-{total_forks}-green?style=for-the-badge&logo=github)
![Contributions](https://img.shields.io/badge/Contributions-{contributions}+-orange?style=for-the-badge&logo=git)

<p align="center">
  <img src="https://github-profile-trophy.vercel.app/?username={username}&theme=radical&no-frame=true&no-bg=false&margin-w=4&row=1" alt="GitHub Trophies" />
</p>
</div>
</details>

---

<details open>
<summary><h2>🔥 Top Repositories</h2></summary>
<div align="center">
"""
        # Add top repositories by stars with cards
        sorted_repos = sorted(repos_data, key=lambda x: x['stargazers_count'], reverse=True)[:3]
        for repo in sorted_repos:
            desc = repo['description'] or 'No description available'
            readme_content += f"""
<a href="{repo['html_url']}">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username={username}&repo={repo['name']}&theme=radical&hide_border=true" />
</a>
"""

        readme_content += """
</div>
</details>

---

<details>
<summary><h2>📝 Latest Blog Posts</h2></summary>

<!-- BLOG-POST-LIST:START -->
- [How to Create an Amazing GitHub Profile](https://example.com/blog1)
- [Top 10 Programming Tips](https://example.com/blog2)
- [Getting Started with Open Source](https://example.com/blog3)
<!-- BLOG-POST-LIST:END -->

</details>

---

<details>
<summary><h2>🎮 When I'm Not Coding</h2></summary>
<div align="center">
<img src="https://media.giphy.com/media/12BYUePgtn7sis/giphy.gif" width="200" height="200">

- 🎮 Playing video games
- 📚 Reading tech blogs
- 🎧 Listening to music
- 🚶 Exploring new places

</div>
</details>

---

<div align="center">

### 🙏 Thanks for visiting my profile!

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%">

<h3>Support Me</h3>
<p>
<a href="https://www.buymeacoffee.com/{username}" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</p>

<p align="center">Created with ❤️ by {self.admin_name} - v{self.version}</p>

</div>
"""
        return readme_content

    def get_tech_color(self, tech):
        """Get color for tech stack badge"""
        colors = {
            "JavaScript": "F7DF1E",
            "Python": "3776AB",
            "HTML": "E34F26",
            "CSS": "1572B6",
            "TypeScript": "3178C6",
            "C++": "00599C",
            "Java": "007396",
            "React": "61DAFB",
            "Node.js": "339933",
            "Express": "000000",
            "Django": "092E20",
            "Flask": "000000",
            "TensorFlow": "FF6F00",
            "MongoDB": "47A248",
            "MySQL": "4479A1",
            "PostgreSQL": "336791",
            "SQLite": "003B57",
            "Redis": "DC382D",
            "Git": "F05032",
            "GitHub": "181717",
            "VS Code": "007ACC",
            "Docker": "2496ED",
            "AWS": "FF9900",
            "Heroku": "430098",
            "Postman": "FF6C37"
        }
        return colors.get(tech, "lightgrey")

    def get_language_color(self, language):
        """Get color for language badge"""
        colors = {
            "Python": "3776AB",
            "JavaScript": "F7DF1E",
            "TypeScript": "3178C6",
            "Java": "007396",
            "C++": "00599C",
            "C#": "239120",
            "PHP": "777BB4",
            "Ruby": "CC342D",
            "Go": "00ADD8",
            "Swift": "FA7343",
            "Kotlin": "7F52FF",
            "Rust": "000000",
            "HTML": "E34F26",
            "CSS": "1572B6",
            "Shell": "4EAA25",
        }
        return colors.get(language, "lightgrey")

    def get_correct_logo_name(self, tech):
        """Get correct logo name for shields.io"""
        # Special mappings for technologies with different logo names
        logo_mappings = {
            "HTML": "html5",
            "CSS": "css3",
            "JavaScript": "javascript",
            "TypeScript": "typescript",
            "Python": "python",
            "Java": "java",
            "C++": "cplusplus",
            "C#": "csharp",
            "PHP": "php",
            "Ruby": "ruby",
            "Go": "go",
            "Swift": "swift",
            "Kotlin": "kotlin",
            "Rust": "rust",
            "Node.js": "nodejs",
            "React": "react",
            "Angular": "angular",
            "Vue.js": "vuejs",
            "Express": "express",
            "Django": "django",
            "Flask": "flask",
            "MongoDB": "mongodb",
            "MySQL": "mysql",
            "PostgreSQL": "postgresql",
            "SQLite": "sqlite",
            "Redis": "redis",
            "Docker": "docker",
            "Kubernetes": "kubernetes",
            "AWS": "amazonaws",
            "Git": "git",
            "GitHub": "github",
            "VS Code": "visualstudiocode",
        }

        # Return the mapped logo name or the lowercase tech name if not in mappings
        return logo_mappings.get(tech, tech.lower())

    def save_and_preview(self, content, username):
        """Save README.md and show preview"""
        try:
            # Save README
            filename = f"README_{username}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            console.print(Panel(f"[bold green]✓ README saved as [bold cyan]{filename}",
                               title="Success",
                               border_style="green",
                               box=box.ROUNDED))

            # Show preview notification
            console.print(Panel("[bold yellow]README Preview (shortened for readability):",
                               title="Preview",
                               border_style="yellow",
                               box=box.ROUNDED))

            # Show shortened preview (first few lines)
            preview_lines = content.split('\n')[:20]
            preview = '\n'.join(preview_lines) + "\n[...more content...]"
            console.print(preview)

            console.print(f"[bold green]✓[/bold green] [cyan]Full README saved to [bold]{filename}[/bold][/cyan]")

        except Exception as e:
            console.print(f"[bold red]Error saving/previewing README: {str(e)}[/bold red]")

def get_user_input(prompt, default=None):
    """Get user input with prompt and optional default value"""
    console = Console()
    if default:
        prompt = f"{prompt} [default: {default}]: "
    else:
        prompt = f"{prompt}: "

    console.print(f"[bold cyan]{prompt}[/bold cyan]", end="")
    response = input()
    return response if response else default

def main():
    # Create generator instance
    generator = GitHubProfileGenerator()

    # Display banner
    generator.display_banner()

    # Get GitHub username with improved input handling
    console.print(Panel("[bold cyan]Welcome to the GitHub Profile Generator![/bold cyan]\n"
                       "[yellow]Generate beautiful GitHub profile READMEs with just a few clicks.[/yellow]",
                       box=box.ROUNDED))

    username = get_user_input("Enter GitHub username")
    while not username:
        console.print("[bold red]Username cannot be empty![/bold red]")
        username = get_user_input("Enter GitHub username")

    # Fetch data and generate README
    console.print(Panel("[bold yellow]Starting GitHub data fetch process...[/bold yellow]",
                       box=box.ROUNDED,
                       border_style="yellow"))

    user_data, repos_data, contributions = generator.fetch_github_data(username)

    if user_data and repos_data:
        console.print(Panel(f"[bold green]✓ Successfully fetched data for [bold cyan]{username}[/bold cyan]![/bold green]",
                           border_style="green",
                           box=box.ROUNDED))

        readme_content = generator.generate_readme(username, user_data, repos_data, contributions)

        if readme_content:
            console.print(Panel("[bold green]✓ README content generated successfully![/bold green]",
                               border_style="green",
                               box=box.ROUNDED))
            generator.save_and_preview(readme_content, username)

            console.print(Panel(f"[bold cyan]Thank you for using GitHub Profile Generator v{generator.version}![/bold cyan]\n"
                               f"[yellow]Your awesome GitHub profile is ready to use![/yellow]\n"
                               f"[green]Created by {generator.admin_name}[/green]",
                               box=box.ROUNDED,
                               border_style="cyan"))
        else:
            console.print("[bold red]Error generating README content[/bold red]")
    else:
        console.print("[bold red]Failed to fetch GitHub data. Please check the username and try again.[/bold red]")

if __name__ == "__main__":
    main()
