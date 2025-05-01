---
layout: post
title: "Aan de Slag met Vibe Coding: van Prompt Engineering tot Web Applicaties"
date: 2025-05-01 00:00:00
description: Vibe coding is een nieuwe trend waarbij je software ontwikkelt zonder zelf een regel code te schrijven. Hiervoor gebruik je AI-tools. De belofte is dat iedereen software kan maken, zelfs zonder enige ervaring met programmeren.
tags: 
categories: 
giscus_comments: false
thumbnail: assets/img/250501.webp
---

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/250501.webp" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Vibe coding is een nieuwe trend waarbij je software ontwikkelt zonder zelf een regel code te schrijven. Hiervoor gebruik je AI-tools. In plaats van te coderen geef je via een tekstinvoer of prompt een beschrijving van de gewenste toepassing. Op basis van deze beschrijving genereert de AI computercode die je kunt uitvoeren om (hopelijk) het gewenste resultaat te bereiken. De uitdaging ligt erin om het gewenste resultaat zo duidelijk mogelijk in een prompt te omschrijven. De belofte is dat iedereen software kan maken, zelfs zonder enige ervaring met programmeren.

De term ['vibe coding' werd in februari geïntroduceerd door Andrej Karpathy](https://x.com/karpathy/status/1886192184808149383), een toonaangevend figuur in het AI-domein. Als AI-onderzoeker stond hij mee aan de wieg van OpenAI (het bedrijf achter ChatGPT) en was hij tot 2022 het hoofd AI bij Tesla. Tegenwoordig richt hij zich vooral op AI-educatie via zijn populaire YouTube-kanaal en zijn bedrijf Eureka Labs. Hij gebruikt de term om aan te geven dat je in plaats van het formele codeerproces eerder je gevoel of 'vibe' volgt tijdens het werken met de AI-tool. Hij gebruikt deze techniek bijvoorbeeld om webapplicaties te bouwen met een framework waar hij niet vertrouwd mee is. Hoewel Karpathy tijdens het vibe coden niet rechtstreeks naar de code kijkt, komt zijn uitgebreide kennis van softwareontwikkeling hem ongetwijfeld van pas. 

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/250501-1.png" class="img-fluid rounded z-depth-1 mx-auto d-block" width="50%" %}
    </div>
</div>

Ook mensen zonder of met beperkte programmeerervaring gaan aan de slag met vibe coding. Kevin Roose, technologiecolumnist voor de New York Times, is hier een voorbeeld van. In een artikel deelde hij [zijn ervaringen met vibe coding](https://www.nytimes.com/2025/02/27/technology/personaltech/vibecoding-ai-software-programming.html). Hij ontwikkelde onder andere LunchBox Buddy, een tool die de inhoud van zijn koelkast analyseert en helpt bij het maken van zijn zoon's brooddoos. Ook maakte hij een applicatie voor zijn Hard Fork podcast co-host voor het onderhoud van diens jacuzzi, maar ondanks het aanvankelijke enthousiasme bleek deze niet erg nuttig te zijn. 

 

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/250501-2.png" class="img-fluid rounded z-depth-1 mx-auto d-block" width="50%" %}
    </div>
</div>

Vibe coding roept ook bezorgdheid op over begrip en verantwoordelijkheid. Ontwikkelaars kunnen AI-gegenereerde code gebruiken zonder de functionaliteit ervan volledig te begrijpen, wat kan leiden tot onopgemerkte bugs, fouten en beveiligingsproblemen. In zijn blogpost [Decoding (and debunking) Hard Fork's Kevin Roose](https://garymarcus.substack.com/p/decoding-and-debunking-hard-forks) bekritiseert AI-onderzoeker Gary Marcus het artikel van Roose. Hij stelt dat Roose in zijn enthousiasme te optimistisch is en softwareontwikkeling te simplistisch voorstelt. Zoals Karpathy al aangaf, is vibe coding vooral geschikt als hobby voor weekendprojectjes en niet voor software die in productie moet draaien. AI-tools maken nog steeds fouten en je kunt nooit volledig vertrouwen op de correctheid van gegenereerde code. 

De voorbeelden van Karpathy en Roose tonen de verschillende contexten aan waarin vibe coding van pas kan komen: voor een ervaren softwareontwikkelaar die snel wil experimenteren met een nieuw framework zonder zich eerst te verdiepen in de syntax, of voor iemand die in zijn vrije tijd met software wil experimenteren. 

Net als bij andere AI-tools is het voor succesvol vibe coding essentieel om duidelijke instructies te kunnen geven (vaak aangeduid als *prompt engineering*). Een aantal vuistregels kunnen je hierbij helpen. Zo is het cruciaal om voldoende context te verstrekken. Waar mensen goed zijn in het inschatten van situaties en ontbrekende informatie zelf kunnen aanvullen, werkt dit anders bij AI. Zonder voldoende context krijg je een soort van gemiddeld antwoord gebaseerd op alles wat op het internet staat. Wat ook kan gebeuren is dat het AI-model ongevraagd een rollenspel start en in een willekeurig karakter kruipt. Het helpt om je prompt stapsgewijs op te bouwen: begin eenvoudig en voeg geleidelijk meer context toe. Zoals met veel vaardigheden geldt ook hier: oefening baart kunst. Begin met experimenten in een vertrouwd gebied. Zo leer je ook herkennen wanneer AI-tools de bal misslaan. In de afbeelding vind je een overzicht dat we hebben samengesteld van deze algemene vuistregels (of *Promptgeboden*) die je helpen om AI-tools effectiever te gebruiken (deze kan je ook downloaden via de pagina [prompten](https://wimcasteels.be/prompt-hulp/)).

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/250501-3.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Om met vibe coding te starten heb je eerst een goed idee nodig van wat je wilt maken. De beste ideeën zijn eenvoudig en lossen een concreet probleem op. Denk bijvoorbeeld aan de LunchBox Buddy applicatie van Kevin Roose. Het is ook slim om te starten met een simpel concept dat je later kan uitbreiden met extra functionaliteit.

De volgende stap is het kiezen van een ontwikkelomgeving. Hier zijn heel veel mogelijkheden, maar mijn persoonlijke voorkeur gaat uit naar Python als programmeertaal. De code is namelijk ook voor beginners leesbaar en dankzij de grote open source community heb je toegang tot enorm veel gratis functionaliteiten. Je kan kiezen tussen het lokaal uitvoeren van de code op je computer of werken in de cloud. Voor lokale ontwikkeling is [Anaconda](https://www.anaconda.com/download) een handige gratis tool die alles voor je installeert en je helpt bij het beheren van je projecten. Als je liever in de cloud werkt, kun je [Github Codespaces](https://github.com/features/codespaces) gebruiken. Je hebt alleen een gratis Github-account nodig en kunt vrijwel meteen beginnen met vibe coding.

De volgende vraag is welke AI-tool je gaat gebruiken voor het genereren van code. Er zijn verschillende opties beschikbaar. De meeste algemene chatbots zijn ook goed in het schrijven van code, dus je kunt je favoriete tool kiezen zoals ChatGPT, Claude of het Franse Mistral. Met de gratis versies kom je al een heel eind, maar als het resultaat niet naar wens is, kan een betalende versie interessant zijn. Deze bieden doorgaans betere resultaten en hebben minder gebruikslimieten. Voor gevorderd gebruik van AI bij het genereren van code is Cursor een goede optie.

Het is interessant om een toepassing te maken met een interface die je aan anderen kunt demonstreren. Van de vele beschikbare opties raad ik Streamlit aan. Hiermee kun je snel en eenvoudig een gebruikersinterface bouwen in Python. Een extra voordeel is dat je je applicatie gratis kunt hosten op de Streamlit cloud, waardoor deze voor iedereen toegankelijk wordt. Als voorbeeld ontwikkelde ik voor een workshop vorig jaar een eenvoudige AI-tool die AI-concepten uitlegt voor verschillende doelgroepen. Probeer het zelf uit op deze link: [Learning AI](https://masterclass2-software-met-genai.streamlit.app/).

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/250501-4.png" class="img-fluid rounded z-depth-1 mx-auto d-block" width="50%" %}
    </div>
</div>

Probeer het nu eens zelf uit! Ga bijvoorbeeld naar je favoriete chatbot en vraag om een Streamlit-applicatie te maken die de BMI van een gebruiker berekent. Ik testte dit met ChatGPT, die niet alleen het Python-script leverde maar ook de instructies voor het downloaden en uitvoeren van Streamlit (je kan het antwoord van ChatGPT [hier](https://chatgpt.com/share/67f64de5-cf30-8004-9aba-466d52689cf9) zien). Als je deze instructies niet meteen krijgt, vraag er dan expliciet naar (vergeet niet: Context is Koning!). Vanaf hier kun je verder experimenteren door extra functionaliteiten toe te voegen of een nieuwe aanpak te kiezen voor het oplossen van problemen waar jij of anderen mee worstelen. 

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/250501-5.png" class="img-fluid rounded z-depth-1 mx-auto d-block" width="50%" %}
    </div>
</div>

Is je nieuwsgierigheid naar vibe coding geprikkeld? Dan is er goed nieuws! De AP Hogeschool organiseert op 29 mei een hands-on workshop over Prompt Engineering en Vibe Coding. Deze workshop sluit naadloos aan bij de hierboven beschreven trend van vibe coding, waarbij je via tekstuele instructies (prompts) software kunt ontwikkelen zonder te programmeren. Tijdens de workshop leer je hoe je effectief communiceert met AI-tools om je ideeën om te zetten in werkende toepassingen. De focus ligt op twee aspecten: het formuleren van doordachte instructies (Prompt Engineering) en het bouwen van softwaretools via AI (Vibe Coding). Je hebt geen programmeerkennis nodig om deel te nemen, geheel in lijn met de democratiserende belofte van vibe coding.

Voor meer informatie over de workshop zie: [Workshop Prompt Engineering & Vibecoding](https://www.ap.be/professionals/opleiding/workshop-prompt-engineering-vibecoding)