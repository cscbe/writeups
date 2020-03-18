Ik heb iets uitgewerkt. Het is een MITM bij een fictief bedrijf: Random Security. Dit bedrijf heeft twee servers opgezet die elk een deel van een geheim (de vlag) bewaren, Tweedledum en Tweedledee. Deze servers vragen een geheime access key om de vlag op te vragen. Wij hebben 'Alice' kunnen plaatsen op een van de servers, dit programma is in staat om al het verkeer van die server te capturen.

Bijgevoegd vind je een minimale setup van de servers. Unzippen en voer
docker-compose up --build
uit. Nu zullen er 3 containers starten die elk een port-publishen:
localhost:4321 -> Tweedledum
localhost:4322 -> Tweedledee
localhost:4323 -> Alice

Tweedledum en Tweedledee zijn de twee webservers die de vlag beschermen, hier kan je naartoe surfen: https://localhost:4321/ en https://localhost:4322/ . Deze bevatten een simpele api om de vlag op te halen.

De derde container, Alice, luistert naar poort 4323, wanneer je een eenvoudige TCP-connectie opent zal zij het resultaat van 'tcpdump -w -' doorsturen. Met
nc localhost 4323 > alice.pcap
krijg je een nieuw bestand dat je kan openen met wireshark.

---

Dit is de challenge, aan de formulering en het verhaaltje is, uiteraard, nog wat werk. Rien heeft kunnen bevestigen dat hij oplosbaar is.

De oplossingsstrategie is de volgende:
De publieke sleutels van Tweedledee en Tweedledum delen een priemgetal, dit betekent dat die met een tool zoals https://github.com/Ganapati/RsaCtfTool zeer eenvoudig te kraken zijn. (Of, zoals ik oorspronkelijk had gedaan: je kan de certificaten 'met de hand' opstellen).
De volgende stap is om Alice te starten en een conversatie tussen tweedledee en tweedledum te triggeren met https://localhost:4321/api/last_accessed_server. De api is beschreven op de homepagina van beide servers.
Als laatste openen we de capture van Alice in wireshark, hier laden we de private keys in die uit RsaCtfTool verkregen zijn. En voila! Wireshark decrypt de ssl connectie tot simpel http. Hieruit kunnen we de access key van de server verkrijgen.
Deze key gebruiken we nu om https://localhost:4321/api/get_secret?key=<key> aan te roepen, hieruit valt de (helft van de) vlag.
Ik sta open voor feedback. Laat maar weten wat er aangepast moet worden om hier een 'echte' challenge van te maken.

Als je tevreden bent van deze challenge, ik heb (blijkbaar) veel inspiratie voor nog challenges. Zo speel ik met het idee voor een leuke SQL-injectie... Of als jullie er zo al een hebben (naar alle waarschijnlijkheid), laat maar weten in welke richtingen ik mijn inspiratie moet sturen.