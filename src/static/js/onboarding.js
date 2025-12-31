/**
 * Onboarding script
 * Friendly onboarding flow designed for children aged 6-12
 */

(function() {
    'use strict';

    let currentStep = 0;
    let onboardingSteps = [];
    let onboardingOverlay = null;

    // Onboarding steps configuration
    const stepsConfig = [
        {
            title: '🌟 Welcome to OiOink!',
            content: 'Learn about money in a fun way! Let\'s take a quick tour.',
            target: null,
            position: 'center',
            icon: '👋'
        },
        {
            title: '💼 Your Wallet',
            content: 'This is your virtual wallet! You can earn coins by completing lessons.',
            target: '[data-onboarding="wallet"]',
            position: 'bottom',
            icon: '💼'
        },
        {
            title: '📚 Learn & Play',
            content: 'Complete fun lessons to learn about money and earn coins!',
            target: '[data-onboarding="lessons"]',
            position: 'bottom',
            icon: '📚'
        },
        {
            title: '🎯 Saving Goals',
            content: 'Set goals and watch your savings grow! See your progress here.',
            target: '[data-onboarding="saving-goals"]',
            position: 'top',
            icon: '🎯'
        },
        {
            title: '💰 Track Spending',
            content: 'Keep track of what you spend to learn about budgeting!',
            target: '[data-onboarding="spending"]',
            position: 'bottom',
            icon: '💰'
        },
        {
            title: '🏆 Achievements',
            content: 'Unlock badges and earn rewards as you learn and save!',
            target: '[data-onboarding="achievements"]',
            position: 'top',
            icon: '🏆'
        },
        {
            title: '🎁 Prize Shop',
            content: 'Use your coins to get cool prizes! Check out the prize shop.',
            target: '[data-onboarding="prizes"]',
            position: 'bottom',
            icon: '🎁'
        },
        {
            title: '🎉 You\'re All Set!',
            content: 'Ready to start your financial learning journey? Let\'s go!',
            target: null,
            position: 'center',
            icon: '🎉'
        }
    ];

    /**
     * Initialize onboarding
     */
    function initOnboarding() {
        if (!document.querySelector('[data-onboarding-active]')) {
            return;
        }

        onboardingSteps = stepsConfig;
        createOnboardingOverlay();
        showStep(0);
    }

    /**
     * Create onboarding overlay
     */
    function createOnboardingOverlay() {
        onboardingOverlay = document.createElement('div');
        onboardingOverlay.id = 'onboarding-overlay';
        onboardingOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 9998;
            transition: opacity 0.3s ease;
        `;
        document.body.appendChild(onboardingOverlay);
    }

    /**
     * Show onboarding step
     */
    function showStep(stepIndex) {
        if (stepIndex < 0 || stepIndex >= onboardingSteps.length) {
            completeOnboarding();
            return;
        }

        currentStep = stepIndex;
        const step = onboardingSteps[stepIndex];
        
        // Remove old onboarding card
        const oldCard = document.getElementById('onboarding-card');
        if (oldCard) {
            oldCard.remove();
        }

        // Create new onboarding card
        const card = createOnboardingCard(step, stepIndex);
        document.body.appendChild(card);

        // Position card
        positionCard(card, step);

        // Highlight target element
        if (step.target) {
            highlightTarget(step.target);
        } else {
            removeHighlights();
        }
    }

    /**
     * Create onboarding card
     */
    function createOnboardingCard(step, stepIndex) {
        const card = document.createElement('div');
        card.id = 'onboarding-card';
        card.style.cssText = `
            position: fixed;
            z-index: 9999;
            background: white;
            border-radius: 20px;
            padding: 2rem;
            max-width: 400px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: cardAppear 0.3s ease-out;
        `;

        const isLast = stepIndex === onboardingSteps.length - 1;
        const isFirst = stepIndex === 0;

        card.innerHTML = `
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 4rem; margin-bottom: 0.5rem;">${step.icon}</div>
                <h3 style="margin-bottom: 0.5rem; color: #333; font-weight: bold;">${step.title}</h3>
                <p style="color: #666; line-height: 1.6; font-size: 1.1rem;">${step.content}</p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 2rem;">
                <div style="flex: 1; text-align: center;">
                    <span style="color: #999; font-size: 0.9rem;">
                        Step ${stepIndex + 1} of ${onboardingSteps.length}
                    </span>
                    <div style="margin-top: 0.5rem;">
                        ${onboardingSteps.map((_, i) => `
                            <span style="
                                display: inline-block;
                                width: 8px;
                                height: 8px;
                                border-radius: 50%;
                                background: ${i === stepIndex ? '#667eea' : '#e9ecef'};
                                margin: 0 3px;
                            "></span>
                        `).join('')}
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                ${!isFirst ? `
                    <button id="onboarding-prev" class="btn btn-outline-secondary" style="flex: 1; border-radius: 10px; padding: 0.75rem;">
                        <i class="bi bi-arrow-left"></i> Previous
                    </button>
                ` : ''}
                <button id="onboarding-next" class="btn btn-primary" style="flex: 1; border-radius: 10px; padding: 0.75rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none;">
                    ${isLast ? 'Get Started!' : 'Next <i class="bi bi-arrow-right"></i>'}
                </button>
            </div>
            <div style="text-align: center; margin-top: 1rem;">
                <button id="onboarding-skip" style="
                    background: none;
                    border: none;
                    color: #999;
                    cursor: pointer;
                    font-size: 0.9rem;
                    text-decoration: underline;
                ">Skip Tour</button>
            </div>
        `;

        // Add event listeners
        card.querySelector('#onboarding-next').addEventListener('click', () => {
            showStep(currentStep + 1);
        });

        if (!isFirst) {
            card.querySelector('#onboarding-prev').addEventListener('click', () => {
                showStep(currentStep - 1);
            });
        }

        card.querySelector('#onboarding-skip').addEventListener('click', () => {
            completeOnboarding();
        });

        return card;
    }

    /**
     * Position card
     */
    function positionCard(card, step) {
        if (step.target && document.querySelector(step.target)) {
            const target = document.querySelector(step.target);
            const rect = target.getBoundingClientRect();
            const cardRect = card.getBoundingClientRect();

            let top, left;

            switch (step.position) {
                case 'top':
                    top = rect.top - cardRect.height - 20;
                    left = rect.left + (rect.width / 2) - (cardRect.width / 2);
                    break;
                case 'bottom':
                    top = rect.bottom + 20;
                    left = rect.left + (rect.width / 2) - (cardRect.width / 2);
                    break;
                case 'left':
                    top = rect.top + (rect.height / 2) - (cardRect.height / 2);
                    left = rect.left - cardRect.width - 20;
                    break;
                case 'right':
                    top = rect.top + (rect.height / 2) - (cardRect.height / 2);
                    left = rect.right + 20;
                    break;
                default:
                    top = window.innerHeight / 2 - cardRect.height / 2;
                    left = window.innerWidth / 2 - cardRect.width / 2;
            }

            // Ensure card is within viewport
            top = Math.max(20, Math.min(top, window.innerHeight - cardRect.height - 20));
            left = Math.max(20, Math.min(left, window.innerWidth - cardRect.width - 20));

            card.style.top = top + 'px';
            card.style.left = left + 'px';
        } else {
            // Center display
            card.style.top = '50%';
            card.style.left = '50%';
            card.style.transform = 'translate(-50%, -50%)';
        }
    }

    /**
     * Highlight target element
     */
    function highlightTarget(selector) {
        removeHighlights();
        const target = document.querySelector(selector);
        if (target) {
            target.style.position = 'relative';
            target.style.zIndex = '9999';
            target.style.transition = 'all 0.3s ease';
            target.classList.add('onboarding-highlight');
        }
    }

    /**
     * Remove highlight
     */
    function removeHighlights() {
        document.querySelectorAll('.onboarding-highlight').forEach(el => {
            el.classList.remove('onboarding-highlight');
            el.style.zIndex = '';
        });
    }

    /**
     * Complete onboarding
     */
    function completeOnboarding() {
        // Remove onboarding elements
        if (onboardingOverlay) {
            onboardingOverlay.style.opacity = '0';
            setTimeout(() => onboardingOverlay.remove(), 300);
        }

        const card = document.getElementById('onboarding-card');
        if (card) {
            card.style.animation = 'cardAppear 0.3s ease-out reverse';
            setTimeout(() => card.remove(), 300);
        }

        removeHighlights();

        // Mark onboarding as completed
        fetch('/myhome/complete-onboarding/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  console.log('Onboarding completed!');
              }
          });
    }

    /**
     * Get Cookie
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Add CSS animations
    if (!document.getElementById('onboarding-styles')) {
        const style = document.createElement('style');
        style.id = 'onboarding-styles';
        style.textContent = `
            @keyframes cardAppear {
                from {
                    transform: scale(0.8) translateY(-20px);
                    opacity: 0;
                }
                to {
                    transform: scale(1) translateY(0);
                    opacity: 1;
                }
            }
            .onboarding-highlight {
                box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.3) !important;
                border-radius: 10px !important;
            }
        `;
        document.head.appendChild(style);
    }

    // Wait for DOM to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initOnboarding);
    } else {
        initOnboarding();
    }
})();


