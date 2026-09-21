# IT Service Desk Runbook

| Field | Value |
|---|---|
| Owner | IT Operations |
| Last updated | June 2025 |
| Classification | Internal |

Contact the IT Service Desk at itsupport@vantagetech.example, x4400, or the #it-help Slack channel. Service Desk hours are 7:00 a.m. to 7:00 p.m. U.S. Central Time, Monday through Friday.

## 1. Password Reset

Vantage uses Okta for single sign-on. Your Okta password is your primary company password.

**Self-service reset**

1. Go to the Okta sign-in page and select **Forgot password?**
2. Enter your work email (first.last@vantagetech.example).
3. Verify your identity using Okta Verify.
4. Choose a new password: at least 14 characters, not reused from your last 10 passwords.
5. Sign out and back in on your laptop so the new password syncs.

**If self-service fails**

- Call the Service Desk at x4400. The technician will verify your identity with a video call and your employee ID before resetting the password.
- IT will **never** ask for your password by email, Slack, or phone.

## 2. Okta MFA

All accounts require multi-factor authentication through Okta Verify.

**Enrolling a new phone**

1. Sign in to Okta on your laptop.
2. Open **Settings > Security Methods**.
3. Select **Set up** next to Okta Verify and scan the QR code with the Okta Verify app.
4. Remove the old device from the list.

**Lost or replaced phone**

- Contact the Service Desk. After identity verification, IT will issue a temporary one-time passcode valid for 4 hours so you can enroll the new device.

**Unexpected MFA prompts**

- If you receive a push notification you did not start, select **No, it's not me** and report it to Security at x4499. Never approve a prompt you did not initiate.

## 3. Laptop Provisioning

**New hires**

1. The hiring manager submits a New Hire request at least 10 business days before the start date.
2. IT assigns a MacBook Pro (Engineering) or MacBook Air (all other departments).
3. The laptop is enrolled in device management and preloaded with CrowdStrike Falcon, the VPN client, Slack, and Google Workspace.
4. Office-based employees pick up their laptop on day one. Remote employees receive it by courier at least two business days before their start date.
5. On first login, the employee sets an Okta password and enrolls in Okta Verify.

**Replacements**

- Laptops are refreshed every 4 years. Damaged devices are replaced after a Service Desk ticket is opened.
- Return old devices using the prepaid shipping label from IT within 14 days.

## 4. VPN Troubleshooting

| Symptom | Steps |
|---|---|
| VPN client will not connect | Confirm internet access; quit and reopen the VPN client; confirm you are signed in to Okta. |
| Repeated MFA prompts | Check the date and time on your laptop are set automatically; re-enroll Okta Verify if needed. |
| Connected but internal sites do not load | Disconnect and reconnect; clear browser cache; run the "Reset network settings" script in Self Service. |
| Slow performance | Switch from Wi-Fi to a wired connection or mobile hotspot; avoid public Wi-Fi for customer data. |
| "Device not compliant" error | Install pending OS updates and confirm CrowdStrike Falcon is running, then reconnect. |

If the issue persists, open a ticket with a screenshot of the error message and the output of the VPN client's **Diagnostics** tab.

## 5. Software Requests

Submit software requests through the Self Service portal. Pre-approved applications install automatically. Other software requires review by IT and Security before installation.

## 6. Escalation

| Priority | Examples | Response Target |
|---|---|---|
| P1 | Company-wide outage, suspected security incident | 15 minutes |
| P2 | Individual cannot work (locked out, laptop failure) | 1 hour |
| P3 | Degraded service, non-urgent request | 1 business day |
