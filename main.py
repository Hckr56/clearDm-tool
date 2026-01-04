import os
import sys
import time
import re
import requests

class LRXTerminal:
    def __init__(self):
        self.width = 120
        self.token = None
        self.dms = []
        self.username = None
        self.user_id = None
        self.uhq8472()

    def uhq8472(self):
        if os.name == 'nt':
            os.system('title LRX - dev by yuzu')

    def uhq3891(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def uhq1029(self, text):
        return re.sub(r'\033\[[0-9;]*m', '', text)

    def uhq5673(self, text):
        visible = self.uhq1029(text)
        padding = (self.width - len(visible)) // 2
        print(' ' * max(padding, 0) + text)

    def uhq7184(self, text, start_color, end_color):
        result = ""
        text_length = len(text)
        
        for i, char in enumerate(text):
            if char == ' ' or char == '\n':
                result += char
                continue
                
            ratio = i / max(text_length - 1, 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            result += f"\033[38;2;{r};{g};{b}m{char}"
            
        result += "\033[0m"
        return result

    def uhq2945(self):
        logo = """
██▓     ██▀███  ▒██   ██▒
▓██▒    ▓██ ▒ ██▒▒▒ █ █ ▒░
▒██░    ▓██ ░▄█ ▒░░  █   ░
▒██░    ▒██▀▀█▄   ░ █ █ ▒ 
░██████▒░██▓ ▒██▒▒██▒ ▒██▒
░ ▒░▓  ░░ ▒▓ ░▒▓░▒▒ ░ ░▓ ░
░ ░ ▒  ░  ░▒ ░ ▒░░░   ░▒ ░
  ░ ░     ░░   ░  ░    ░  
    ░  ░   ░      ░    ░
"""
        start_color = (255, 240, 240)
        end_color = (248, 217, 255)
        
        lines = logo.strip().split('\n')
        result_lines = []
        
        for i, line in enumerate(lines):
            progress = i / max(len(lines) - 1, 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)
            colored_line = self.uhq7184(line, (r, g, b), (r, g, b))
            result_lines.append(colored_line)
        
        return result_lines

    def uhq6328(self):
        sparkles = "✦ ･ ﾟ ✧ * ･ ﾟ ✦ ･ ﾟ ✧ * ･ ﾟ ✦ * ･ ﾟ ✧ ･ ﾟ * ✦ ･ ﾟ ✧"
        return f"\033[38;2;255;240;240m{sparkles}\033[0m"

    def uhq4791(self, show_status=False, online=False):
        self.uhq3891()
        print()
        logo_lines = self.uhq2945()
        for line in logo_lines:
            self.uhq5673(line)
        print()
        self.uhq5673(self.uhq6328())
        print()
        
        if show_status:
            if online and self.username:
                status = f"\033[38;2;100;255;100m● Online\033[0m \033[38;2;248;217;255minto\033[0m \033[38;2;255;240;240m{self.username}\033[0m"
            else:
                status = f"\033[38;2;255;100;100m● Offline\033[0m"
            self.uhq5673(status)
            print()
        print()

    def uhq9012(self, token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                'https://discord.com/api/v9/users/@me',
                headers=headers
            )
            
            if response.status_code == 200:
                user_data = response.json()
                self.username = user_data.get('username', 'Unknown')
                self.user_id = user_data.get('id')
                return True
            else:
                return False
        except:
            return False

    def uhq3457(self, token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                'https://discord.com/api/v9/users/@me/channels',
                headers=headers
            )
            
            if response.status_code == 200:
                channels = response.json()
                self.dms = [ch for ch in channels if ch['type'] == 1]
                return True
            else:
                return False
        except:
            return False

    def uhq8765(self, channel_id):
        headers = {
            'Authorization': self.token
        }
        
        deleted_count = 0
        before = None
        message_counter = 0
        
        try:
            while True:
                time.sleep(0.1)
                
                params = {'limit': 100}
                if before:
                    params['before'] = before
                
                response = requests.get(
                    f'https://discord.com/api/v9/channels/{channel_id}/messages',
                    headers=headers,
                    params=params
                )
                
                if response.status_code != 200:
                    break
                
                messages = response.json()
                
                if not messages:
                    break
                
                messages_deleted = False
                
                for msg in messages:
                    if not isinstance(msg, dict):
                        continue
                    
                    author = msg.get('author', {})
                    author_id = author.get('id')
                    
                    if author_id == self.user_id:
                        delete_response = requests.delete(
                            f'https://discord.com/api/v9/channels/{channel_id}/messages/{msg["id"]}',
                            headers=headers
                        )
                        
                        if delete_response.status_code == 204:
                            deleted_count += 1
                            messages_deleted = True
                            message_counter += 1
                            
                            if message_counter <= 5:
                                time.sleep(0.9)
                            else:
                                time.sleep(1.7)
                                
                        elif delete_response.status_code == 429:
                            retry_after = delete_response.json().get('retry_after', 1)
                            time.sleep(retry_after + 0.3)
                            delete_response = requests.delete(
                                f'https://discord.com/api/v9/channels/{channel_id}/messages/{msg["id"]}',
                                headers=headers
                            )
                            if delete_response.status_code == 204:
                                deleted_count += 1
                                messages_deleted = True
                                message_counter += 1
                                
                                if message_counter <= 5:
                                    time.sleep(0.9)
                                else:
                                    time.sleep(1.7)
                        elif delete_response.status_code == 403:
                            pass
                
                if not messages_deleted:
                    break
                
                if len(messages) < 100:
                    break
                
                before = messages[-1]['id']
            
            return deleted_count
        except Exception as e:
            return deleted_count

    def uhq1548(self):
        self.uhq4791(show_status=True, online=True)
        
        if not self.dms:
            msg = f"\033[38;2;255;240;240m✦ No DMs found\033[0m"
            self.uhq5673(msg)
            print()
            time.sleep(2)
            return False
        
        clear_text = f"\033[38;2;248;217;255mClear DM? (y/n)\033[0m"
        self.uhq5673(clear_text)
        print()
        
        prompt = f"\033[38;2;248;217;255m✧･ﾟ \033[38;2;255;240;240mchoice\033[38;2;248;217;255m ･ﾟ✧ → \033[0m"
        visible_prompt = self.uhq1029(prompt)
        padding = (self.width - len(visible_prompt)) // 2
        choice = input(' ' * padding + prompt).strip().lower()
        
        if choice == 'y' or choice == 'yes':
            self.uhq4791(show_status=True, online=True)
            
            for i, dm in enumerate(self.dms, 1):
                recipient = dm['recipients'][0] if dm.get('recipients') else {}
                username = recipient.get('username', 'Unknown')
                
                dm_text = f"\033[38;2;255;240;240m[{i}]\033[0m \033[38;2;248;217;255m{username}\033[0m"
                self.uhq5673(dm_text)
            
            print()
            print()
            
            select_text = f"\033[38;2;248;217;255mSelect DM number to clear (or 'all')\033[0m"
            self.uhq5673(select_text)
            print()
            
            num_prompt = f"\033[38;2;248;217;255m✧･ﾟ \033[38;2;255;240;240mnumber\033[38;2;248;217;255m ･ﾟ✧ → \033[0m"
            visible = self.uhq1029(num_prompt)
            padding = (self.width - len(visible)) // 2
            num = input(' ' * padding + num_prompt).strip()
            
            if num.lower() == 'all':
                self.uhq4791(show_status=True, online=True)
                msg = f"\033[38;2;248;217;255m✧ Clearing all DMs... ✧\033[0m"
                self.uhq5673(msg)
                print()
                total = 0
                for idx, dm in enumerate(self.dms, 1):
                    status = f"\033[38;2;255;240;240m[{idx}/{len(self.dms)}] Clearing...\033[0m"
                    self.uhq5673(status)
                    count = self.uhq8765(dm['id'])
                    total += count
                    time.sleep(0.5)
                print()
                if total == 0:
                    finish = f"\033[38;2;248;217;255m✧ Finished - No messages to delete ✧\033[0m"
                else:
                    finish = f"\033[38;2;100;255;100m✧ Finished! ({total} messages deleted) ✧\033[0m"
                self.uhq5673(finish)
                time.sleep(2)
                bye = "\033[38;2;248;217;255m✧･ﾟ Bye bye! ･ﾟ✧\033[0m"
                print()
                self.uhq5673(bye)
                time.sleep(1.5)
                sys.exit(0)
            elif num.isdigit() and 1 <= int(num) <= len(self.dms):
                dm = self.dms[int(num) - 1]
                self.uhq4791(show_status=True, online=True)
                msg = f"\033[38;2;248;217;255m✧ Clearing DM... ✧\033[0m"
                self.uhq5673(msg)
                count = self.uhq8765(dm['id'])
                print()
                if count == 0:
                    finish = f"\033[38;2;248;217;255m✧ Finished - No messages to delete ✧\033[0m"
                else:
                    finish = f"\033[38;2;100;255;100m✧ Finished! ({count} messages deleted) ✧\033[0m"
                self.uhq5673(finish)
                time.sleep(2)
                bye = "\033[38;2;248;217;255m✧･ﾟ Bye bye! ･ﾟ✧\033[0m"
                print()
                self.uhq5673(bye)
                time.sleep(1.5)
                sys.exit(0)
        else:
            self.uhq4791(show_status=True, online=False)
            msg = f"\033[38;2;248;217;255m✧ Disconnected ✧\033[0m"
            self.uhq5673(msg)
            time.sleep(1.5)
            self.token = None
            self.username = None
            self.dms = []
            return False

    def uhq6942(self):
        while True:
            self.uhq4791(show_status=True, online=False)
            
            prompt = f"\033[38;2;248;217;255m✧･ﾟ \033[38;2;255;240;240mtoken\033[38;2;248;217;255m ･ﾟ✧ → \033[0m"
            visible_prompt = self.uhq1029(prompt)
            padding = (self.width - len(visible_prompt)) // 2
            token = input(' ' * padding + prompt).strip()
            
            if token.lower() in ['q', 'quit', 'exit']:
                bye = "\033[38;2;248;217;255m✧･ﾟ Bye bye! ･ﾟ✧\033[0m"
                self.uhq5673(bye)
                time.sleep(1.5)
                break
            
            if token:
                if self.uhq9012(token):
                    self.token = token
                    self.uhq4791(show_status=True, online=True)
                    
                    msg = f"\033[38;2;248;217;255m✧ Loading DMs... ✧\033[0m"
                    self.uhq5673(msg)
                    time.sleep(1)
                    
                    if self.uhq3457(token):
                        continue_loop = self.uhq1548()
                        if not continue_loop:
                            continue
                    else:
                        msg = f"\033[38;2;255;100;100m✦ Error loading DMs ✦\033[0m"
                        self.uhq5673(msg)
                        time.sleep(2)
                else:
                    self.uhq4791(show_status=True, online=False)
                    msg = f"\033[38;2;255;100;100m✦ Invalid token! ✦\033[0m"
                    self.uhq5673(msg)
                    time.sleep(2)

if __name__ == "__main__":
    try:
        terminal = LRXTerminal()
        terminal.uhq6942()
    except KeyboardInterrupt:
        print("\n\033[38;2;248;217;255m✧･ﾟ Bye bye! ･ﾟ✧\033[0m")
        sys.exit(0)