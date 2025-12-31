/**
 * Achievement notification system
 * Display notifications when users unlock new achievements
 */

(function() {
    'use strict';

    let notificationQueue = [];
    let isShowingNotification = false;

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

    /**
     * Check unnotified achievements
     */
    function checkUnnotifiedAchievements() {
        fetch('/achievements/api/unnotified/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.achievements && data.achievements.length > 0) {
                // Add achievements to queue
                data.achievements.forEach(achievement => {
                    notificationQueue.push(achievement);
                });
                
                // If no notification currently showing, start showing
                if (!isShowingNotification) {
                    showNextNotification();
                }
            }
        })
        .catch(error => {
            console.error('Error fetching unnotified achievements:', error);
        });
    }

    /**
     * Show next notification
     */
    function showNextNotification() {
        if (notificationQueue.length === 0) {
            isShowingNotification = false;
            return;
        }

        isShowingNotification = true;
        const achievement = notificationQueue.shift();
        showAchievementNotification(achievement);
    }

    /**
     * Show achievement notification
     */
    function showAchievementNotification(achievement) {
        // Create notification container
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: linear-gradient(135deg, ${achievement.color || '#FFD700'} 0%, rgba(255, 215, 0, 0.8) 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            min-width: 350px;
            max-width: 400px;
            animation: slideInRight 0.5s ease-out;
            cursor: pointer;
        `;

        notification.innerHTML = `
            <div class="d-flex align-items-start">
                <div style="font-size: 4rem; margin-right: 1rem; animation: bounce 1s ease-in-out infinite;">
                    ${achievement.icon || '🏆'}
                </div>
                <div style="flex: 1;">
                    <h4 style="margin-bottom: 0.5rem; font-weight: bold; font-size: 1.3rem;">
                        Achievement Unlocked! 🎉
                    </h4>
                    <h5 style="margin-bottom: 0.5rem; font-weight: 600; font-size: 1.1rem;">
                        ${achievement.name}
                    </h5>
                    <p style="margin-bottom: 0.75rem; opacity: 0.95; font-size: 0.95rem; line-height: 1.4;">
                        ${achievement.description}
                    </p>
                    ${achievement.coin_reward > 0 ? `
                        <div style="background: rgba(255, 255, 255, 0.2); padding: 0.5rem 1rem; border-radius: 10px; display: inline-block;">
                            <span style="font-size: 1.2rem; font-weight: bold;">
                                ⭐ +${achievement.coin_reward} Coins!
                            </span>
                        </div>
                    ` : ''}
                </div>
                <button class="btn-close btn-close-white" style="opacity: 0.8; margin-left: 0.5rem;" onclick="closeAchievementNotification(this, ${achievement.id});"></button>
            </div>
        `;

        document.body.appendChild(notification);

        // Add CSS animations
        if (!document.getElementById('achievement-notification-styles')) {
            const style = document.createElement('style');
            style.id = 'achievement-notification-styles';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                }
                @keyframes bounce {
                    0%, 100% {
                        transform: translateY(0);
                    }
                    50% {
                        transform: translateY(-10px);
                    }
                }
                .achievement-notification:hover {
                    transform: scale(1.02);
                    transition: transform 0.2s ease;
                }
            `;
            document.head.appendChild(style);
        }

        // Click notification to go to achievement detail
        notification.addEventListener('click', function(e) {
            if (!e.target.classList.contains('btn-close')) {
                window.location.href = `/achievements/${achievement.achievement_id}/`;
            }
        });

        // Auto close (after 5 seconds)
        setTimeout(function() {
            if (notification.parentNode) {
                notification.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(function() {
                    if (notification.parentNode) {
                        notification.remove();
                    }
                    markAchievementNotified(achievement.id);
                    // Show next notification
                    setTimeout(showNextNotification, 500);
                }, 300);
            }
        }, 5000);
    }

    /**
     * Mark achievement as notified
     */
    function markAchievementNotified(achievementId) {
        fetch(`/achievements/api/${achievementId}/mark-notified/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Achievement marked as notified');
            }
        })
        .catch(error => {
            console.error('Error marking achievement as notified:', error);
        });
    }

    /**
     * Close achievement notification
     */
    function closeAchievementNotification(button, achievementId) {
        const notification = button.closest('.achievement-notification');
        if (notification) {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(function() {
                if (notification.parentNode) {
                    notification.remove();
                }
                markAchievementNotified(achievementId);
                // Show next notification
                setTimeout(showNextNotification, 500);
            }, 300);
        }
    }

    // Expose functions to global scope (for inline onclick)
    window.markAchievementNotified = markAchievementNotified;
    window.closeAchievementNotification = closeAchievementNotification;

    // Check unnotified achievements after page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            // Delay check slightly to ensure page is fully loaded
            setTimeout(checkUnnotifiedAchievements, 1000);
        });
    } else {
        setTimeout(checkUnnotifiedAchievements, 1000);
    }

    // Periodic check (check every 30 seconds)
    setInterval(checkUnnotifiedAchievements, 30000);
})();

