// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "nav-prompten",
          title: "prompten",
          description: "De 7 Promptgeboden om verantwoord gebruik te maken van AI-tools.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/prompt-hulp/";
          },
        },{id: "nav-lezingen",
          title: "lezingen",
          description: "Informatie over aankomende en voorbije lezingen.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/lezingen/";
          },
        },{id: "nav-cv",
          title: "cv",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-publicaties",
          title: "publicaties",
          description: "Wetenschappelijke publicaties van Wim Casteels",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-",
          title: "",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/contact/";
          },
        },{id: "post-gemiste-kansen-in-het-belgisch-charter-voor-verantwoord-ai-gebruik",
      
        title: "Gemiste kansen in het Belgisch charter voor verantwoord AI-gebruik",
      
      description: "",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/Knack-charter/";
        
      },
    },{id: "post-ai-zoekmachines-ondermijnen-verdienmodel-internet",
      
        title: "AI-zoekmachines ondermijnen verdienmodel internet",
      
      description: "",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/De-Tijd-AI-Zoekmachines/";
        
      },
    },{id: "post-na-aankondiging-diependaele-over-copilot-wordt-vlaanderen-te-afhankelijk-van-een-amerikaans-technologiebedrijf",
      
        title: "Na aankondiging Diependaele over Copilot: wordt Vlaanderen te afhankelijk van een Amerikaans technologiebedrijf?...",
      
      description: "",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/Knack-copilot/";
        
      },
    },{id: "post-verklein-je-werkelijk-je-ecologische-voetafdruk-door-minder-vriendelijk-te-zijn-tegen-chatgpt",
      
        title: "Verklein je werkelijk je ecologische voetafdruk door minder vriendelijk te zijn tegen ChatGPT?...",
      
      description: "",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/Knack-voetafdruk/";
        
      },
    },{id: "post-de-onzichtbare-manager-hoe-ai-de-werkvloer-vormgeeft",
      
        title: "De Onzichtbare Manager: Hoe AI de Werkvloer Vormgeeft",
      
      description: "AI neemt steeds vaker de rol van manager over, met verstrekkende gevolgen voor de werkvloer. Van het screenen van sollicitanten tot het monitoren van werknemers - algoritmes bepalen steeds meer hoe we werken. Wat betekent deze onzichtbare manager voor de toekomst van werk?",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/AI-work/";
        
      },
    },{id: "post-aan-de-slag-met-vibe-coding-van-prompt-engineering-tot-web-applicaties",
      
        title: "Aan de Slag met Vibe Coding: van Prompt Engineering tot Web Applicaties",
      
      description: "Vibe coding is een nieuwe trend waarbij je software ontwikkelt zonder zelf een regel code te schrijven. Hiervoor gebruik je AI-tools. De belofte is dat iedereen software kan maken, zelfs zonder enige ervaring met programmeren.",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/vibe-coding/";
        
      },
    },{id: "post-waarom-onderzoek-naar-artificiële-algemene-intelligentie-contraproductief-kan-zijn-eos-wetenschap",
      
        title: 'Waarom onderzoek naar artificiële algemene intelligentie contraproductief kan zijn | EOS Wetenschap <svg width="1.2rem" height="1.2rem" top=".5rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
      
      description: "Het doel van&amp;nbsp;artificiële intelligentie is altijd geweest om machines te maken die menselijke intelligentie simuleren. Toch kan het nastreven ervan onbed...",
      section: "Posts",
      handler: () => {
        
          window.open("https://www.eoswetenschap.eu/technologie/waarom-onderzoek-naar-artificiele-algemene-intelligentie-contraproductief-kan-zijn", "_blank");
        
      },
    },{id: "post-de-opkomst-van-ai-therapeuten",
      
        title: "De opkomst van AI therapeuten",
      
      description: "AI neemt steeds meer de rol van therapeut op zich in onze digitale samenleving. Van ELIZA in de jaren &#39;60 tot moderne chatbots als ChatGPT en Character.AI, steeds meer mensen delen hun diepste emoties met AI. Maar terwijl sommigen hier verlichting in vinden, waarschuwen experts voor de risico&#39;s van deze nieuwe vorm van &#39;therapie&#39;.",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/AI-therapie/";
        
      },
    },{id: "post-ai-als-bewaker-van-fort-europa",
      
        title: "AI als bewaker van fort Europa",
      
      description: "De inzet van AI voor grensbewaking en immigratiecontrole is een snel groeiende toepassing van deze technologie. Europa investeert miljarden in de ontwikkeling en implementatie van AI-systemen die moeten helpen bij het monitoren en controleren van migratie. Deze ontwikkeling roept belangrijke ethische en praktische vragen op over effectiviteit, mensenrechten en discriminatie.",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/fort-europa/";
        
      },
    },{id: "post-hoe-vervuilend-is-ai-de-afdruk-van-ai-vaia-vlaamse-ai-academie",
      
        title: 'Hoe vervuilend is AI? De afdruk van AI - VAIA - Vlaamse AI... <svg width="1.2rem" height="1.2rem" top=".5rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
      
      description: "Generatieve AI werd razendsnel populair dankzij gebruiksvriendelijke interfaces die de complexe infrastructuur verbergen. Maar in al hun eenvoud gebruiken deze tools enorme hoeveelheden energie, water en grondstoffen. Wim Casteels van AP Hogeschool bespreekt de grootste problemen.",
      section: "Posts",
      handler: () => {
        
          window.open("https://www.vaia.be/nl/blog/hoe-vervuilend-is-ai", "_blank");
        
      },
    },{id: "post-de-groeiende-ecologische-voetafdruk-van-ai",
      
        title: "De Groeiende Ecologische Voetafdruk van AI",
      
      description: "De opkomst van AI verbruikt enorme hoeveelheden grondstoffen, waardoor grote technologiebedrijven hun klimaatdoelstellingen niet kunnen halen.",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/ecologische-duurzaamheid/";
        
      },
    },{id: "post-wie-ligt-er-nog-wakker-van-de-veiligheid-van-ai",
      
        title: "Wie ligt er nog wakker van de veiligheid van AI?",
      
      description: "Na de komst van ChatGPT stond AI veiligheid hoog op de (politieke) agenda maar dat lijkt met de AI Action top in Parijs vorige week definitief verleden tijd.",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/AI-Veiligheid/";
        
      },
    },{id: "post-eerste-stap-van-de-ai-act-binnenkort-allemaal-ai-geletterd",
      
        title: "Eerste stap van de AI Act. Binnenkort allemaal AI geletterd?",
      
      description: "Begin februari trad de eerste fase van de AI Act in werking. Deze Europese wetgeving verbiedt AI-systemen met een onacceptabel risico en stelt verplichtingen over AI-geletterdheid.",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/AI-Act-stap-1/";
        
      },
    },{id: "post-maakt-ai-ons-dommer",
      
        title: "Maakt AI ons dommer?",
      
      description: "AI maakt ons productiever op het werk, maar wat is het effect op de mensen die deze tools gebruiken?",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/dommer/";
        
      },
    },{id: "post-chinese-startup-zet-ai-en-financiële-wereld-op-zijn-kop",
      
        title: "Chinese startup zet AI en financiële wereld op zijn kop",
      
      description: "",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/deepseek/";
        
      },
    },{id: "post-sociale-media-voor-jongeren",
      
        title: "Sociale media voor jongeren",
      
      description: "",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/social-media/";
        
      },
    },{id: "news-de-eerste-aflevering-van-de-genius-podcast-staat-online-intelligent-omgaan-met-artificiële-intelligentie-met-caroline-van-cauwelaert-ceo-van-epcon-en-wim-casteels",
          title: 'De eerste aflevering van de Genius Podcast staat online: Intelligent omgaan met artificiële...',
          description: "",
          section: "News",},{id: "news-het-boek-het-masker-van-ai-verschijnt-op-21-oktober-bij-lannoo-campus-iedereen-is-welkom-voor-de-boekvoorstelling-op-23-oktober-om-19u-op-campus-noord-van-de-ap-hogeschool",
          title: 'Het boek Het masker van AI verschijnt op 21 oktober bij Lannoo Campus....',
          description: "",
          section: "News",},{id: "projects-project-1",
          title: 'project 1',
          description: "with background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_project/";
            },},{id: "projects-project-2",
          title: 'project 2',
          description: "a project with a background image and giscus comments",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_project/";
            },},{id: "projects-project-3-with-very-long-name",
          title: 'project 3 with very long name',
          description: "a project that redirects to another website",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_project/";
            },},{id: "projects-project-4",
          title: 'project 4',
          description: "another without an image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_project/";
            },},{id: "projects-project-5",
          title: 'project 5',
          description: "a project with a background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_project/";
            },},{id: "projects-project-6",
          title: 'project 6',
          description: "a project with no image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_project/";
            },},{id: "projects-project-7",
          title: 'project 7',
          description: "with background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/7_project/";
            },},{id: "projects-project-8",
          title: 'project 8',
          description: "an other project with a background image and giscus comments",
          section: "Projects",handler: () => {
              window.location.href = "/projects/8_project/";
            },},{id: "projects-project-9",
          title: 'project 9',
          description: "another project with an image 🎉",
          section: "Projects",handler: () => {
              window.location.href = "/projects/9_project/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%63%61%73%74%65%65%6C%73.%77%69%6D@%67%6D%61%69%6C.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/wim-casteels-213720b4", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=fyQ8MmcAAAAJ", "_blank");
        },
      },{
        id: 'social-custom_social',
        title: 'Custom_social',
        section: 'Socials',
        handler: () => {
          window.open("https://www.ap.be/expert/wim-casteels", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
