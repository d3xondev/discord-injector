# Discord Injector

This repository is retained for educational and defensive research purposes.

## Disclaimer

This project is intended only for lawful security education, malware-analysis
practice, and defensive review of how client-side injection techniques can be
identified and prevented.

Do not use this project to access, collect, intercept, transmit, or store
Discord tokens, credentials, session data, personal information, or any other
data from systems or accounts that you do not own or do not have explicit
permission to test.

Unauthorized credential collection, account compromise, persistence,
exfiltration, or deployment against third-party systems is illegal and
unethical. The repository owner and contributors are not responsible for misuse.

## Intended Use

Acceptable uses include:

- Reviewing code for defensive education
- Understanding why client-side credential interception is dangerous
- Building detection rules in a controlled lab
- Studying how to remove or neutralize unsafe injection code
- Learning how to protect local Discord installations from tampering

Do not use this repository as a ready-to-run tool against other users.

## Security Note

If a webhook, token, credential, or other secret was ever committed to this
repository, assume it is compromised. Remove it from the repository, rotate or
revoke it at the provider, and avoid reusing it anywhere else.

## Responsible Handling

If you fork or study this code, keep it in a controlled environment and remove
any real endpoints, secrets, or account-specific data before publishing changes.
