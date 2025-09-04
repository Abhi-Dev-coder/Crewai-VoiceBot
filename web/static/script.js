class VoiceBotApp {
    constructor() {
        this.isListening = false;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        
        this.initElements();
        this.initSpeechRecognition();
        this.bindEvents();
        this.loadLogs();
    }
    
    initElements() {
        this.micButton = document.getElementById('micButton');
        this.voiceStatus = document.getElementById('voiceStatus');
        this.textInput = document.getElementById('textInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.logsList = document.getElementById('logsList');
        this.refreshLogs = document.getElementById('refreshLogs');
        this.errorModal = document.getElementById('errorModal');
        this.errorMessage = document.getElementById('errorMessage');
        this.closeModal = document.querySelector('.close');
    }
    
    initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
        } else if ('SpeechRecognition' in window) {
            this.recognition = new SpeechRecognition();
        } else {
            this.showError('Speech recognition is not supported in this browser');
            this.micButton.disabled = true;
            return;
        }
        
        // Check for microphone access
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                console.log('Microphone access granted');
                // Stop the stream immediately as we just needed to check permission
                stream.getTracks().forEach(track => track.stop());
            })
            .catch(err => {
                console.error('Microphone access error:', err);
                this.showError('Microphone access denied. Please enable microphone access in your browser settings.');
                this.micButton.disabled = true;
            });
        
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';
        // Increase timeout for recognition
        this.recognition.maxAlternatives = 1;
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.micButton.classList.add('listening');
            this.voiceStatus.textContent = 'Listening... Speak now!';
        };
        
        this.recognition.onresult = (event) => {
            if (event.results.length > 0 && event.results[0].length > 0) {
                const transcript = event.results[0][0].transcript;
                console.log('Speech recognized:', transcript);
                if (transcript.trim()) {
                    this.textInput.value = transcript;
                    this.processQuery(transcript);
                } else {
                    this.showError('Empty speech detected. Please try speaking more clearly.');
                }
            } else {
                this.showError('No speech detected. Please try again.');
            }
        };
        
        this.recognition.onerror = (event) => {
            this.stopListening();
            let errorMsg = 'Speech recognition error';
            console.error('Speech recognition error:', event.error);
            
            switch(event.error) {
                case 'no-speech':
                    errorMsg = 'No speech detected. Please try again and speak clearly into your microphone.';
                    break;
                case 'audio-capture':
                    errorMsg = 'Microphone access denied or unavailable. Please check your microphone connection and browser permissions.';
                    break;
                case 'not-allowed':
                    errorMsg = 'Microphone permission denied. Please allow microphone access in your browser settings.';
                    break;
                case 'network':
                    errorMsg = 'Network error occurred. Please check your internet connection.';
                    break;
                case 'aborted':
                    errorMsg = 'Speech recognition was aborted. Please try again.';
                    break;
                default:
                    errorMsg = `Speech recognition error: ${event.error}. Please try again or use text input instead.`;
            }
            
            this.showError(errorMsg);
        };
        
        this.recognition.onend = () => {
            this.stopListening();
        };
    }
    
    bindEvents() {
        this.micButton.addEventListener('click', () => this.toggleListening());
        this.sendButton.addEventListener('click', () => this.handleTextSubmit());
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleTextSubmit();
        });
        this.refreshLogs.addEventListener('click', () => this.loadLogs());
        this.closeModal.addEventListener('click', () => this.hideError());
        
        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target === this.errorModal) this.hideError();
        });
    }
    
    toggleListening() {
        if (this.isListening) {
            this.recognition.stop();
        } else {
            // Check microphone access before starting recognition
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    // Stop the stream immediately as we just needed to check permission
                    stream.getTracks().forEach(track => track.stop());
                    
                    try {
                        console.log('Starting speech recognition...');
                        this.voiceStatus.textContent = 'Starting speech recognition...';
                        this.recognition.start();
                    } catch (error) {
                        console.error('Error starting speech recognition:', error);
                        this.showError('Could not start speech recognition: ' + error.message);
                    }
                })
                .catch(err => {
                    console.error('Microphone access error:', err);
                    this.showError('Microphone access denied. Please enable microphone access in your browser settings.');
                });
        }
    }
    
    stopListening() {
        this.isListening = false;
        this.micButton.classList.remove('listening');
        this.voiceStatus.textContent = 'Ready to listen';
    }
    
    handleTextSubmit() {
        const text = this.textInput.value.trim();
        if (text) {
            this.processQuery(text);
        }
    }
    
    async processQuery(query) {
        if (!query.trim()) return;
        
        this.addMessage(query, 'user');
        this.textInput.value = '';
        this.setProcessingState(true);
        
        try {
            const response = await fetch('/api/process-voice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: query })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage(data.assistant_response, 'assistant');
                this.speakResponse(data.assistant_response);
                this.loadLogs(); // Refresh logs after successful interaction
            } else {
                this.showError(data.error || 'Failed to process query');
            }
        } catch (error) {
            this.showError('Network error. Please check your connection.');
            console.error('Error processing query:', error);
        } finally {
            this.setProcessingState(false);
        }
    }
    
    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.textContent = content;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    speakResponse(text) {
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        
        // Try to use a female voice if available
        const voices = this.synthesis.getVoices();
        const femaleVoice = voices.find(voice => 
            voice.name.toLowerCase().includes('female') || 
            voice.name.toLowerCase().includes('samantha') ||
            voice.name.toLowerCase().includes('alex')
        );
        
        if (femaleVoice) {
            utterance.voice = femaleVoice;
        }
        
        utterance.onstart = () => {
            this.voiceStatus.textContent = 'Speaking...';
        };
        
        utterance.onend = () => {
            this.voiceStatus.textContent = 'Ready to listen';
        };
        
        this.synthesis.speak(utterance);
    }
    
    setProcessingState(isProcessing) {
        this.sendButton.disabled = isProcessing;
        this.micButton.disabled = isProcessing;
        
        if (isProcessing) {
            this.micButton.classList.add('processing');
            this.voiceStatus.textContent = 'Processing...';
            this.sendButton.innerHTML = '<div class="loading"></div>';
        } else {
            this.micButton.classList.remove('processing');
            this.voiceStatus.textContent = 'Ready to listen';
            this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        }
    }
    
    async loadLogs() {
        try {
            const response = await fetch('/api/get-logs');
            const data = await response.json();
            
            if (data.success) {
                this.displayLogs(data.logs);
            } else {
                this.logsList.innerHTML = '<p>Error loading logs</p>';
            }
        } catch (error) {
            this.logsList.innerHTML = '<p>Failed to load logs</p>';
            console.error('Error loading logs:', error);
        }
    }
    
    displayLogs(logs) {
        if (!logs || logs.length === 0) {
            this.logsList.innerHTML = '<p>No interactions yet</p>';
            return;
        }
        
        const logsHtml = logs.reverse().map(log => `
            <div class="log-item">
                <div class="log-query">${this.escapeHtml(log.query)}</div>
                <div class="log-response">${this.escapeHtml(log.response.substring(0, 100))}${log.response.length > 100 ? '...' : ''}</div>
                <div class="log-time">${new Date(log.timestamp).toLocaleString()}</div>
            </div>
        `).join('');
        
        this.logsList.innerHTML = logsHtml;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    showError(message) {
        this.errorMessage.textContent = message;
        this.errorModal.style.display = 'block';
    }
    
    hideError() {
        this.errorModal.style.display = 'none';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VoiceBotApp();
});

// Handle page visibility changes to manage speech synthesis
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        speechSynthesis.cancel();
    }
});