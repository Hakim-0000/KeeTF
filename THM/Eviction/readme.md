MITRE ATT&CK Navigation Layer : https://static-labs.tryhackme.cloud/sites/eviction/

What is a technique used by the APT to both perform recon and gain initial access? 
- spearphishing link
-> karena disini yang dipertanyakan adalah melakukan recon dan mendapat initial access, jadi pastinya menggunakan phishing seperti yang sudah di highlight

Sunny identified that the APT might have moved forward from the recon phase. Which accounts might the APT compromise while developing resources?
- Email Accounts
-> dalam hal ini adalah email, karena dalam proses resource development APT mengumpulkan data yang dapat digunakan untuk menyerang target seperti informasi tentang domain, web service, dan tentunya untuk mendapat akses perlu email account. selain itu, dalam tahap ini APT juga memilih tools yang tepat yang dapat digunakan sesuai dengan data resource yang telah dikumpulkan.

E-corp has found that the APT might have gained initial access using social engineering to make the user execute code for the threat actor. Sunny wants to identify if the APT was also successful in execution. What two techniques of user execution should Sunny look out for?
- Malicious File and Malicious Link
-> dalam hal ini, kita langsung fokus ke proses execution, dan dalam hal ini teknik user execution yang digunakan adalah melalui Malicious Link dan Malicious File

If the above technique was successful, which scripting interpreters should Sunny search for to identify successful execution?
- PowerShell and Windows Command Shell
-> dalam hal ini kita masih di section execution. Jika execution berhasil, kita dapat cek melalui Windows Command Shell dan juga PowerShell untuk melihat semua proses yang tereksekusi.

While looking at the scripting interpreters identified in Q4, Sunny found some obfuscated scripts that changed the registry. Assuming these changes are for maintaining persistence, which registry keys should Sunny observe to track these changes?
- Registry Run Key
-> dalam kasus ini, kita menemukan sebuah script yang membuat perubahan pada registry dan bisa diasumsikan hal ini bertujuan untuk maintain persistence, maka dari MITRE ATT&CK navigator kita bisa langsung melihat pada bagian Persistence dan melihat pada bagian Boot or Logon Autostart Exec, dan kita menemukan Registry Run Keys.

Sunny identified that the APT executes system binaries to evade defences. Which system binary's execution should Sunny scrutinize for proxy execution?
- Rundll32
-> disini kita menemukan bahwa APT exec bin untuk evade defence, jadi kita bisa fokus ke section Defense Evasion, dan kita akan menemukan binary execution untuk defense evasion yang dilakukan APT28 adalah System Binary Proxy Execution dan menggunakan Rundll32

Sunny identified tcpdump on one of the compromised hosts. Assuming this was placed there by the threat actor, which technique might the APT be using here for discovery?
- Network Sniffing
-> karena di salah satu compromised hosts kita menemukan tcpdump, kita bisa pergi ke section Discovery, dan disitu terdapat beberapa teknik yang digunakan APT, namun yang berkaitan dengan tcpdump adalah Network Sniffing

It looks like the APT achieved lateral movement by exploiting remote services. Which remote services should Sunny observe to identify APT activity traces? 
- SMB/Windows Admin Shares
-> disini kita menemukan bahwa APT melakukan lateral movement dengan exploiting remote service, jika kita pergi ke section Lateral Movement, kita akan menemukan bahwa APT menggunakan SMB/Windows Admin Shares untuk melancarkan lateral movement nya.

It looked like the primary goal of the APT was to steal intellectual property from E-corp's information repositories. Which information repository can be the likely target of the APT?
- Sharepoint
-> disini sepertinya tujuan utama APT adalah mencuri IP dari repositori informasi milik E-corp, jika kita pergi ke section Collection, kita akan menemukan Data From Information Repositories, dan yang di target APT adalah sharepoint. Sharepoint adalah web based collaborative platform yang digunakan sebagai document management dan storage system serta sharing informasi lewat intranet, implementasi internal applications, dan juga implementasi bisnis process. Sharepoint dari Microsoft dan integrated dengan Ms365

Although the APT had collected the data, it could not connect to the C2 for data exfiltration. To thwart any attempts to do that, what types of proxy might the APT use?
- External Proxy and Multi-hop Proxy
-> karena APT tidak dapat connect ke C2 servernya untuk exfil data, maka dia akan menggunakan proxy, yang mana adalah External Proxy dan Multi-hop Proxy.
