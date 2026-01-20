// Mobile Menu Toggle
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        navToggle.classList.toggle('active');
    });
}

// Close mobile menu when a link is clicked
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        navToggle.classList.remove('active');
    });
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const target = document.querySelector(targetId);
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Navbar background on scroll
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 50) {
        navbar.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = 'none';
    }

    lastScroll = currentScroll;
});

// Active navigation link on scroll
const sections = document.querySelectorAll('section[id]');

function setActiveNavLink() {
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelectorAll('.nav-links a').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

window.addEventListener('scroll', setActiveNavLink);

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.section, .service-card, .news-item, .media-item, .contact-card').forEach(element => {
    element.style.opacity = '0';
    observer.observe(element);
});

// Dynamic year for footer
const yearSpan = document.getElementById('year');
if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
}

// Load latest news items from nieuws.html on homepage
async function loadLatestNews() {
    const newsGrid = document.querySelector('#nieuws .news-grid');
    if (!newsGrid) return;

    try {
        const response = await fetch('nieuws.html');
        const html = await response.text();

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        const newsEntries = doc.querySelectorAll('.news-entry');
        const latestThree = Array.from(newsEntries).slice(0, 3);

        if (latestThree.length === 0) return;

        newsGrid.innerHTML = '';

        latestThree.forEach(entry => {
            const date = entry.querySelector('.news-entry-date')?.textContent || '';
            const title = entry.querySelector('.news-entry-content h2 a')?.textContent ||
                         entry.querySelector('.news-entry-content h2')?.textContent || '';
            const description = entry.querySelector('.news-entry-content p')?.textContent || '';

            const newsItem = document.createElement('article');
            newsItem.className = 'news-item';
            newsItem.innerHTML = `
                <span class="news-date">${date}</span>
                <h3>${title}</h3>
                <p>${description}</p>
                <a href="nieuws.html" class="news-link">Lees meer</a>
            `;

            newsGrid.appendChild(newsItem);
        });

        // Re-observe new items for fade-in animation
        newsGrid.querySelectorAll('.news-item').forEach(item => {
            item.style.opacity = '0';
            observer.observe(item);
        });

    } catch (error) {
        console.log('Could not load news items:', error);
    }
}

// Load news when DOM is ready
loadLatestNews();

// News filter functionality
const filterButtons = document.querySelectorAll('.filter-btn');
const newsEntries = document.querySelectorAll('.news-entry');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Update active button
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        const filter = button.dataset.filter;

        // Filter news entries
        newsEntries.forEach(entry => {
            if (filter === 'all' || entry.dataset.category === filter) {
                entry.style.display = '';
            } else {
                entry.style.display = 'none';
            }
        });
    });
});
