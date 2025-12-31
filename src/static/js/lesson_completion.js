/**
 * Lesson completion flow enhancement script
 * Handles completion confirmation dialog and reward animation
 */

(function() {
    'use strict';

    // Wait for DOM to load
    document.addEventListener('DOMContentLoaded', function() {
        const completeForm = document.getElementById('lesson-complete-form');
        const completeButton = document.getElementById('lesson-complete-btn');
        
        if (completeForm && completeButton) {
            // Prevent default form submission
            completeForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Show confirmation dialog
                showCompletionConfirmModal(completeForm);
            });
        }

        // Check URL parameters, if completed=1, show reward animation
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('completed') === '1') {
            // Delay display slightly to ensure page is loaded
            setTimeout(function() {
                showRewardAnimation();
            }, 500);
        }
    });

    /**
     * Show completion confirmation dialog
     */
    function showCompletionConfirmModal(form) {
        const lessonTitle = document.querySelector('.lesson-cover-card-body h1')?.textContent || 'this lesson';
        const coinReward = form.dataset.coinReward || '0';
        const isCompleted = form.dataset.isCompleted === 'true';
        
        // Show different modals based on status
        let modalHTML;
        
        if (isCompleted) {
            // Confirmation dialog for canceling completion
            modalHTML = `
                <div class="modal fade" id="lessonCompleteConfirmModal" tabindex="-1" aria-labelledby="lessonCompleteConfirmModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content" style="border-radius: 20px; border: none;">
                            <div class="modal-header text-center" style="background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%); color: white; border-radius: 20px 20px 0 0;">
                                <h4 class="modal-title w-100" id="lessonCompleteConfirmModalLabel">
                                    <span style="font-size: 3rem; display: block; margin-bottom: 0.5rem;">🔄</span>
                                    Reset Progress?
                                </h4>
                            </div>
                            <div class="modal-body text-center p-4">
                                <p class="lead mb-3">Are you sure you want to reset this lesson's progress?</p>
                                <div class="alert alert-info mb-3" style="border-radius: 15px;">
                                    <div style="font-size: 2rem;" class="mb-2">📚</div>
                                    <strong>The lesson will be marked as "In Progress"</strong>
                                    <p class="small mb-0 mt-2">You can complete it again to earn rewards!</p>
                                </div>
                                <p class="text-muted small">Note: Your earned coins will not be removed.</p>
                            </div>
                            <div class="modal-footer justify-content-center" style="border: none;">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" style="border-radius: 10px;">
                                    <i class="bi bi-x-circle"></i> Cancel
                                </button>
                                <button type="button" class="btn btn-warning btn-lg" id="confirmCompleteBtn" style="border-radius: 10px;">
                                    <i class="bi bi-arrow-counterclockwise"></i> Yes, Reset!
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Confirmation dialog for completing lesson
            modalHTML = `
                <div class="modal fade" id="lessonCompleteConfirmModal" tabindex="-1" aria-labelledby="lessonCompleteConfirmModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content" style="border-radius: 20px; border: none;">
                            <div class="modal-header text-center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 20px 20px 0 0;">
                                <h4 class="modal-title w-100" id="lessonCompleteConfirmModalLabel">
                                    <span style="font-size: 3rem; display: block; margin-bottom: 0.5rem;">🎉</span>
                                    Complete Lesson?
                                </h4>
                            </div>
                            <div class="modal-body text-center p-4">
                                <p class="lead mb-3">Are you sure you want to mark this lesson as completed?</p>
                                ${coinReward > 0 ? `
                                    <div class="alert alert-warning mb-3" style="border-radius: 15px;">
                                        <div style="font-size: 2rem;" class="mb-2">⭐</div>
                                        <strong>You will earn <span style="font-size: 1.5rem; color: #ffc107;">${coinReward}</span> virtual coins!</strong>
                                    </div>
                                ` : ''}
                                <p class="text-muted small">You can always review this lesson later.</p>
                            </div>
                            <div class="modal-footer justify-content-center" style="border: none;">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" style="border-radius: 10px;">
                                    <i class="bi bi-x-circle"></i> Cancel
                                </button>
                                <button type="button" class="btn btn-success btn-lg" id="confirmCompleteBtn" style="border-radius: 10px;">
                                    <i class="bi bi-check-circle"></i> Yes, Complete!
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        // Remove existing modal
        const existingModal = document.getElementById('lessonCompleteConfirmModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('lessonCompleteConfirmModal'));
        modal.show();

        // Confirm button click event
        document.getElementById('confirmCompleteBtn').addEventListener('click', function() {
            // Close modal
            modal.hide();
            
            // Submit form
            form.submit();
        });

        // Clean up after modal closes
        document.getElementById('lessonCompleteConfirmModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }

    /**
     * Show reward animation
     */
    function showRewardAnimation() {
        // Create reward animation container
        const rewardContainer = document.createElement('div');
        rewardContainer.id = 'reward-animation-container';
        rewardContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9999;
            pointer-events: none;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        // Get reward information
        const coinReward = document.querySelector('[data-coin-reward]')?.dataset.coinReward || '0';
        const lessonTitle = document.querySelector('.lesson-cover-card-body h1')?.textContent || 'Lesson';

        // Create reward card
        const rewardCard = document.createElement('div');
        rewardCard.style.cssText = `
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem;
            border-radius: 30px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: rewardCardAppear 0.5s ease-out;
            max-width: 500px;
            width: 90%;
        `;

        rewardCard.innerHTML = `
            <div style="font-size: 5rem; margin-bottom: 1rem; animation: celebrate 1s ease-in-out infinite;">🎉</div>
            <h2 style="margin-bottom: 1rem; font-weight: bold;">Congratulations!</h2>
            <p style="font-size: 1.2rem; margin-bottom: 2rem;">You completed "${lessonTitle}"!</p>
            ${coinReward > 0 ? `
                <div style="background: rgba(255, 255, 255, 0.2); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">⭐</div>
                    <div style="font-size: 2rem; font-weight: bold;">+${coinReward} Coins!</div>
                    <p style="margin-top: 0.5rem; opacity: 0.9;">Added to your wallet</p>
                </div>
            ` : ''}
            <button id="closeRewardAnimation" style="
                background: white;
                color: #667eea;
                border: none;
                padding: 0.75rem 2rem;
                border-radius: 25px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 1rem;
                pointer-events: auto;
            ">Awesome!</button>
        `;

        rewardContainer.appendChild(rewardCard);
        document.body.appendChild(rewardContainer);

        // Add CSS animations
        if (!document.getElementById('reward-animation-styles')) {
            const style = document.createElement('style');
            style.id = 'reward-animation-styles';
            style.textContent = `
                @keyframes rewardCardAppear {
                    from {
                        transform: scale(0.5) translateY(-50px);
                        opacity: 0;
                    }
                    to {
                        transform: scale(1) translateY(0);
                        opacity: 1;
                    }
                }
                @keyframes celebrate {
                    0%, 100% {
                        transform: scale(1) rotate(0deg);
                    }
                    25% {
                        transform: scale(1.1) rotate(-5deg);
                    }
                    75% {
                        transform: scale(1.1) rotate(5deg);
                    }
                }
                @keyframes coinFly {
                    0% {
                        transform: translateY(0) scale(1);
                        opacity: 1;
                    }
                    100% {
                        transform: translateY(-100px) scale(0.5);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        // Close button event
        document.getElementById('closeRewardAnimation').addEventListener('click', function() {
            rewardContainer.style.animation = 'rewardCardAppear 0.3s ease-out reverse';
            setTimeout(function() {
                rewardContainer.remove();
                // Remove URL parameter
                const url = new URL(window.location);
                url.searchParams.delete('completed');
                window.history.replaceState({}, '', url);
            }, 300);
        });

        // Auto close after 3 seconds
        setTimeout(function() {
            const closeBtn = document.getElementById('closeRewardAnimation');
            if (closeBtn && rewardContainer.parentNode) {
                closeBtn.click();
            }
        }, 3000);
    }
})();

