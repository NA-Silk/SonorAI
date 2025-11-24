let uploadedFile = null;
let generatedTab = null;

// Function to ensure page fills screen properly
function updateScale() {
   
}

// File upload handler
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        uploadedFile = file;
        console.log('File uploaded:', file.name);
        
        // Display file name
        const fileNameEl = document.getElementById('file-name');
        if (fileNameEl) {
            fileNameEl.textContent = file.name;
        }
        
        // Save file to localStorage
        const fileData = {
            name: file.name,
            size: file.size,
            type: file.type,
            uploadDate: new Date().toISOString(),
            tabGenerated: false
        };
        
        // Get existing files
        let savedFiles = JSON.parse(localStorage.getItem('sonoraiFiles') || '[]');
        savedFiles.push(fileData);
        localStorage.setItem('sonoraiFiles', JSON.stringify(savedFiles));
        
        // Simulate processing
        setTimeout(() => {
            generatedTab = 'Generated tablature for ' + file.name;
            fileData.tabGenerated = true;
            // Update the file in storage
            savedFiles = JSON.parse(localStorage.getItem('sonoraiFiles') || '[]');
            const index = savedFiles.findIndex(f => f.name === file.name && f.uploadDate === fileData.uploadDate);
            if (index !== -1) {
                savedFiles[index] = fileData;
                localStorage.setItem('sonoraiFiles', JSON.stringify(savedFiles));
            }
            alert('Audio file processed! Tablature generated.');
            // Refresh My Files page if we're on it
            if (window.location.pathname.includes('myfiles.html')) {
                displayFiles();
            }
        }, 1000);
    }
}

// Download handler
function handleDownload() {
    if (generatedTab) {
        // Create a download link
        const blob = new Blob([generatedTab], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'music-tab.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        alert('Tablature downloaded!');
    } else {
        alert('Please upload an audio file first.');
    }
}

// Login handler
function handleLogin() {
    const email = document.getElementById('email-input').value;
    const password = document.getElementById('password-input').value;
    
    if (email && password) {
        console.log('Login attempt:', { email, password });
        alert('Login successful!');
        window.location.href = 'home.html';
    } else {
        alert('Please enter both email and password.');
    }
}

// Email validation function 
function isValidEmail(email) {
   
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!emailRegex.test(email)) {
        return false;
    }
    
    
    const parts = email.split('@');
    const domain = parts[1];
    
 
    if (!domain.includes('.')) {
        return false;
    }
    
   
    const domainParts = domain.split('.');
    const tld = domainParts[domainParts.length - 1];
    
    if (tld.length < 2) {
        return false;
    }
    
    
    if (domainParts.length < 2 || domainParts[0].length === 0) {
        return false;
    }
    
    return true;
}

// Handle Sign up
function handleSignUp() {
    const email = document.getElementById('signup-email-input').value.trim();
    const firstName = document.getElementById('signup-firstname-input').value.trim();
    const lastName = document.getElementById('signup-lastname-input').value.trim();
    const password = document.getElementById('signup-password-input').value;
    
     
    if (!email || !firstName || !lastName || !password) {
        alert('Please fill in all fields.');
        return;
    }
    
     
    if (!isValidEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }
    
     
    if (password.length < 5) {
        alert('Password must be at least 5 characters long.');
        return;
    }
    
    
    const users = JSON.parse(localStorage.getItem('sonoraiUsers') || '[]');
    const existingUser = users.find(u => u.email === email);
    
    if (existingUser) {
        alert('An account with this email already exists.');
        return;
    }
    
     
    const userData = {
        email,
        firstName,
        lastName,
        password, // In production, this should be hashed
        signUpDate: new Date().toISOString()
    };
    
    users.push(userData);
    localStorage.setItem('sonoraiUsers', JSON.stringify(users));
    
    // Automatically log in the new user
    localStorage.setItem('currentUser', JSON.stringify({
        email: userData.email,
        firstName: userData.firstName,
        lastName: userData.lastName
    }));
    
    alert('Account created successfully!');
    window.location.href = 'home.html';
}

// Display files in My Files page
function displayFiles() {
    const filesBody = document.querySelector('.files-body');
    if (!filesBody) return;
    
    const savedFiles = JSON.parse(localStorage.getItem('sonoraiFiles') || '[]');
    
    if (savedFiles.length === 0) {
        filesBody.innerHTML = '<p class="files-empty-message">No files uploaded yet. Upload a file from the Home page!</p>';
        return;
    }
    
    // Sort files by upload date ( 
    savedFiles.sort((a, b) => new Date(b.uploadDate) - new Date(a.uploadDate));
    
    filesBody.innerHTML = savedFiles.map((file, index) => {
        const uploadDate = new Date(file.uploadDate);
        const formattedDate = uploadDate.toLocaleDateString() + ' ' + uploadDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const fileSize = (file.size / 1024).toFixed(2) + ' KB';
        
        return `
            <div class="file-item">
                <div class="file-item-info">
                    <p class="file-item-name">${file.name}</p>
                    <p class="file-item-details">${formattedDate} • ${fileSize}</p>
                    ${file.tabGenerated ? '<span class="tab-badge">Tab Generated</span>' : ''}
                </div>
                <div class="file-item-actions">
                    ${file.tabGenerated ? `<button onclick="downloadFile('${file.name}')" class="file-download-btn">Download</button>` : ''}
                    <button onclick="deleteFile(${index})" class="file-delete-btn">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

// Download file function
function downloadFile(fileName) {
    const savedFiles = JSON.parse(localStorage.getItem('sonoraiFiles') || '[]');
    const file = savedFiles.find(f => f.name === fileName && f.tabGenerated);
    
    if (file) {
        const blob = new Blob(['Generated tablature for ' + fileName], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName.replace(/\.[^/.]+$/, '') + '-tab.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Delete file function
function deleteFile(index) {
    if (confirm('Are you sure you want to delete this file?')) {
        const savedFiles = JSON.parse(localStorage.getItem('sonoraiFiles') || '[]');
        savedFiles.splice(index, 1);
        localStorage.setItem('sonoraiFiles', JSON.stringify(savedFiles));
        displayFiles();
    }
}

// Add test files for demonstration
function addTestFiles() {
    const testFiles = [
        {
            name: 'guitar_solo.mp3',
            size: 2456789,
            type: 'audio/mpeg',
            uploadDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
            tabGenerated: true
        },
        {
            name: 'acoustic_song.wav',
            size: 5123456,
            type: 'audio/wav',
            uploadDate: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 days ago
            tabGenerated: true
        },
        {
            name: 'jazz_improvisation.mp3',
            size: 3890123,
            type: 'audio/mpeg',
            uploadDate: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
            tabGenerated: false
        }
    ];
    
    // Only add test files if no files exist
    const existingFiles = JSON.parse(localStorage.getItem('sonoraiFiles') || '[]');
    if (existingFiles.length === 0) {
        localStorage.setItem('sonoraiFiles', JSON.stringify(testFiles));
    }
}

 
document.addEventListener('DOMContentLoaded', function() {
    updateScale();
    window.addEventListener('resize', updateScale);
    
    // Add test files for demonstration
    addTestFiles();
    
    // Display files if on My Files page
    if (window.location.pathname.includes('myfiles.html') || document.querySelector('.files-body')) {
        displayFiles();
    }
});
