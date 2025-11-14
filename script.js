// ============================================
// BULANDTECH WEBSITE - COMPLETE JAVASCRIPT
// WITH FORMSPREE INTEGRATION
// ============================================

// Preloader
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    setTimeout(() => {
        preloader.classList.add('hidden');
    }, 2000); /* Increased timeout to allow new animations to complete */
});

// Initialize AOS Animation
AOS.init({
    duration: 1000,
    once: true,
    offset: 100
});

// Navbar Scroll Effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile Menu Toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Active Navigation Link on Scroll
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Typing Animation
const typedTextSpan = document.querySelector('.typed-text');
const textArray = [
    'Websites 🌐',
    'Mobile Apps 📱',
    'Music Beats 🎵',
    'Videos 🎬',
    'Graphic Designs 🎨',
    'Digital Marketing 📊',
    'Creative Solutions 💡'
];
const typingDelay = 100;
const erasingDelay = 50;
const newTextDelay = 2000;
let textArrayIndex = 0;
let charIndex = 0;

function type() {
    if (charIndex < textArray[textArrayIndex].length) {
        typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, typingDelay);
    } else {
        setTimeout(erase, newTextDelay);
    }
}

function erase() {
    if (charIndex > 0) {
        typedTextSpan.textContent = textArray[textArrayIndex].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(erase, erasingDelay);
    } else {
        textArrayIndex++;
        if (textArrayIndex >= textArray.length) textArrayIndex = 0;
        setTimeout(type, typingDelay + 500);
    }
}

if (typedTextSpan) {
    setTimeout(type, newTextDelay + 250);
}

// Counter Animation
const counters = document.querySelectorAll('.counter');
const speed = 200;

const counterAnimation = () => {
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
        const increment = target / speed;

        if (count < target) {
            counter.innerText = Math.ceil(count + increment);
            setTimeout(() => counterAnimation(), 1);
        } else {
            counter.innerText = target + '+';
        }
    });
};

// Intersection Observer for Counter
const counterSection = document.querySelector('.about');
let counterAnimated = false;

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !counterAnimated) {
            counterAnimation();
            counterAnimated = true;
        }
    });
}, { threshold: 0.5 });

if (counterSection) {
    counterObserver.observe(counterSection);
}

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ============================================
// FORMSPREE CONTACT FORM INTEGRATION
// ============================================

const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form data
        const formData = new FormData(contactForm);

        // Show loading state
        const submitBtn = contactForm.querySelector('.submit-btn');
        const btnText = submitBtn.querySelector('span');
        const originalText = btnText.textContent;
        btnText.textContent = 'Sending...';
        submitBtn.disabled = true;

        try {
            // ============================================
            // ⚠️ IMPORTANT: FORMSPREE SETUP REQUIRED
            // ============================================
            // STEP 1: Go to https://formspree.io/
            // STEP 2: Sign up for FREE account (No credit card needed)
            // STEP 3: Click "New Form" button
            // STEP 4: Give your form a name: "BulandTech Contact"
            // STEP 5: Copy your Form ID (looks like: xpwananz or abc123xyz)
            // STEP 6: Replace 'YOUR_FORMSPREE_ID' below with your Form ID
            // 
            // Example: 
            // If your endpoint is: https://formspree.io/f/xpwananz
            // Then your Form ID is: xpwananz
            // So replace line below with: const FORMSPREE_ID = 'xpwananz';
            // ============================================
            
            const FORMSPREE_ID = 'YOUR_FORMSPREE_ID'; // 👈 YAHAN APNA FORMSPREE ID DALEIN
            
            // ============================================
            // AFTER SETUP: Messages aapke email par aayenge!
            // - FormSpree dashboard mein bhi dikhengi
            // - Email notifications automatically aayengi
            // - Spam protection built-in hai
            // ============================================

            // Send form to FormSpree
            const response = await fetch(`https://formspree.io/f/xvgvqlkp`, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (response.ok) {
                // ✅ SUCCESS! Form submitted successfully
                formMessage.className = 'form-message success';
                formMessage.textContent = '✅ धन्यवाद! आपका message भेज दिया गया है। हम जल्द ही आपसे संपर्क करेंगे। | Thank you! Your message has been sent successfully. We will contact you soon.';
                
                // Reset form fields
                contactForm.reset();

                // Auto-hide message after 7 seconds
                setTimeout(() => {
                    formMessage.className = 'form-message';
                    formMessage.textContent = '';
                }, 7000);

            } else {
                // ❌ ERROR: Handle FormSpree errors
                const data = await response.json();
                if (data.errors) {
                    formMessage.className = 'form-message error';
                    formMessage.textContent = '❌ Error: ' + data.errors.map(error => error.message).join(', ');
                } else {
                    throw new Error('Form submission failed');
                }
            }

        } catch (error) {
            // ❌ CATCH: Network or other errors
            formMessage.className = 'form-message error';
            formMessage.textContent = '❌ क्षमा करें, कुछ गलत हो गया। कृपया सीधे हमसे संपर्क करें: +91 82659 99762 | Sorry, something went wrong. Please contact us directly: +91 82659 99762';
            console.error('Form submission error:', error);
            
            // Log error details for debugging
            console.log('Error details:', {
                message: error.message,
                formspreeID: FORMSPREE_ID === 'YOUR_FORMSPREE_ID' ? '⚠️ NOT CONFIGURED!' : 'Configured'
            });
        } finally {
            // Reset button state (always runs)
            btnText.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}

// Scroll to Top Button
const scrollTopBtn = document.getElementById('scrollTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollTopBtn.classList.add('visible');
    } else {
        scrollTopBtn.classList.remove('visible');
    }
});

if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Parallax Effect for Hero Section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.hero-shape');
    
    parallaxElements.forEach((element, index) => {
        const speed = 0.5 + (index * 0.1);
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Add hover effect to service cards
const serviceCards = document.querySelectorAll('.service-card');
serviceCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.zIndex = '10';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.zIndex = '1';
    });
});

// Add animation to pricing cards on hover
const pricingCards = document.querySelectorAll('.pricing-card');
pricingCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        if (!this.classList.contains('featured')) {
            this.style.background = 'white';
            this.style.transform = 'translateY(-10px) scale(1.02)';
        }
    });
    
    card.addEventListener('mouseleave', function() {
        if (!this.classList.contains('featured')) {
            this.style.background = '';
            this.style.transform = '';
        }
    });
});

// Animate elements on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.service-card, .pricing-card, .contact-item');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;
        
        if (elementTop < window.innerHeight && elementBottom > 0) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
};

// Initial setup for scroll animations
document.querySelectorAll('.service-card, .pricing-card, .contact-item').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
});

window.addEventListener('scroll', animateOnScroll);
animateOnScroll(); // Run on page load

// Add ripple effect to buttons
const buttons = document.querySelectorAll('.btn, .service-btn, .pricing-btn, .submit-btn');

buttons.forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .btn, .service-btn, .pricing-btn, .submit-btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation
const validateForm = () => {
    const inputs = contactForm.querySelectorAll('input, select, textarea');
    let isValid = true;

    inputs.forEach(input => {
        if (input.hasAttribute('required') && !input.value.trim()) {
            input.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            input.style.borderColor = '#e2e8f0';
        }
    });

    return isValid;
};

// Real-time form validation
if (contactForm) {
    const inputs = contactForm.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.style.borderColor = '#ef4444';
            } else {
                this.style.borderColor = '#10b981';
            }
        });

        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.style.borderColor = '#10b981';
            }
        });
    });
}

// Lazy loading for images (if you add images later)
const lazyLoadImages = () => {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
};

lazyLoadImages();

// Add floating animation to icons
const floatingIcons = document.querySelectorAll('.icon-float');
floatingIcons.forEach((icon, index) => {
    icon.style.animationDelay = `${index * 0.5}s`;
});

// Performance: Debounce scroll events
let scrollTimeout;
window.addEventListener('scroll', () => {
    if (scrollTimeout) {
        window.cancelAnimationFrame(scrollTimeout);
    }
    
    scrollTimeout = window.requestAnimationFrame(() => {
        // Scroll-dependent code here
    });
});

// Easter egg: Console message
console.log('%c🚀 BulandTech - Complete Digital Solutions', 'color: #6366f1; font-size: 20px; font-weight: bold;');
console.log('%cWebsite & App Development | Music Production | Video Editing | Graphic Design | Digital Marketing', 'color: #8b5cf6; font-size: 14px;');
console.log('%cContact: +91 82659 99762 | Email: Theuntoldtales8265@gmail.com', 'color: #ec4899; font-size: 12px;');

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    // ESC key to close mobile menu
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
});

// Print page info
console.log('%cDeveloped with ❤️ by BulandTech', 'color: #10b981; font-size: 16px; font-weight: bold;');

// Service worker registration (for PWA - optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when you create service-worker.js
        // navigator.serviceWorker.register('/service-worker.js')
        //     .then(registration => console.log('SW registered:', registration))
        //     .catch(error => console.log('SW registration failed:', error));
    });
}

// Download App Modal Functionality
const downloadAppLink = document.getElementById('download-app-link');
const downloadModal = document.getElementById('downloadModal');
const closeButton = document.querySelector('.close-button');

if (downloadAppLink && downloadModal && closeButton) {
    downloadAppLink.addEventListener('click', (e) => {
        e.preventDefault();
        downloadModal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
    });

    closeButton.addEventListener('click', () => {
        downloadModal.style.display = 'none';
        document.body.style.overflow = ''; // Restore scrolling
    });

    window.addEventListener('click', (e) => {
        if (e.target === downloadModal) {
            downloadModal.style.display = 'none';
            document.body.style.overflow = ''; // Restore scrolling
        }
    });
}
