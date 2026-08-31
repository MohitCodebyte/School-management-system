// ========================================
// Animations JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initScrollReveal();
    initCounterAnimation();
    initParallax();
    initHoverEffects();
    initFloatingShapes();
    initGradientGlow();
});

// Scroll Reveal Animation using Intersection Observer
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    revealElements.forEach(element => {
        revealObserver.observe(element);
    });
}

// Counter Animation
function initCounterAnimation() {
    const counters = document.querySelectorAll('.counter');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.dataset.target || counter.textContent);
                const duration = parseInt(counter.dataset.duration || 2000);
                animateCounter(counter, target, duration);
                counterObserver.unobserve(counter);
            }
        });
    }, {
        threshold: 0.5
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

function animateCounter(element, target, duration) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// Parallax Effect
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', throttle(() => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = parseFloat(element.dataset.speed || 0.5);
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    }, 16));
}

// Card Hover Effects
function initHoverEffects() {
    const hoverCards = document.querySelectorAll('.card-hover, .card-lift');
    
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Floating Shapes Animation
function initFloatingShapes() {
    const shapes = document.querySelectorAll('.floating-shape');
    
    shapes.forEach((shape, index) => {
        shape.style.animationDelay = `${index * 2}s`;
    });
}

// Gradient Glow Effect
function initGradientGlow() {
    const glowElements = document.querySelectorAll('.glow-effect');
    
    glowElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.classList.add('glowing');
        });
        
        element.addEventListener('mouseleave', function() {
            this.classList.remove('glowing');
        });
    });
}

// Staggered Entrance Animation
function initStaggeredEntrance() {
    const staggerContainers = document.querySelectorAll('.stagger-container');
    
    staggerContainers.forEach(container => {
        const items = container.querySelectorAll('.stagger-item');
        
        const staggerObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    items.forEach((item, index) => {
                        setTimeout(() => {
                            item.classList.add('active');
                        }, index * 100);
                    });
                    staggerObserver.unobserve(container);
                }
            });
        }, {
            threshold: 0.1
        });
        
        staggerObserver.observe(container);
    });
}

// Button Ripple Effect
function initRippleEffect() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
                left: ${x}px;
                top: ${y}px;
                width: 100px;
                height: 100px;
                margin-left: -50px;
                margin-top: -50px;
            `;
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Add ripple animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth Page Transitions
function initPageTransitions() {
    const links = document.querySelectorAll('a:not([target="_blank"])');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if it's a hash link or external link
            if (href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto')) {
                return;
            }
            
            e.preventDefault();
            
            document.body.classList.add('page-transition-out');
            
            setTimeout(() => {
                window.location.href = href;
            }, 300);
        });
    });
}

// Loading Animation for Images
function initImageLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        imageObserver.observe(img);
    });
}

// Text Typing Animation
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Morphing Animation
function initMorphAnimation() {
    const morphElements = document.querySelectorAll('.morph');
    
    morphElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            this.style.transform = 'scale(1.1) rotate(5deg)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });
}

// Progress Bar Animation
function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar-fill');
    
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const target = bar.dataset.progress || bar.style.width;
                bar.style.width = '0%';
                
                setTimeout(() => {
                    bar.style.width = target;
                }, 100);
                
                progressObserver.unobserve(bar);
            }
        });
    }, {
        threshold: 0.5
    });
    
    progressBars.forEach(bar => {
        progressObserver.observe(bar);
    });
}

// Throttle function for performance
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize all animations on page load
window.addEventListener('load', function() {
    initStaggeredEntrance();
    initRippleEffect();
    initPageTransitions();
    initImageLoading();
    initMorphAnimation();
    initProgressBars();
});

// Export functions for global use
window.typeWriter = typeWriter;
