let currentFilename = null;
let isRawView = true;

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('resumeFile');
    const uploadStatus = document.getElementById('uploadStatus');

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset UI
        resetUI();
        
        // Show loading state
        uploadStatus.innerHTML = '<div class="alert alert-info">Extracting text from document...</div>';
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Store filename for later use
                currentFilename = result.filename;
                
                // Show success message
                uploadStatus.innerHTML = '<div class="alert alert-success">Document processed successfully!</div>';
                
                // Display extracted text
                const extractedContent = document.getElementById('extractedContent');
                const extractedText = document.getElementById('extractedText');
                extractedText.textContent = result.text;
                extractedContent.classList.remove('d-none');
                
                // Show processing options
                document.getElementById('processingOptions').classList.remove('d-none');
                
                // Show processing results container
                document.getElementById('processingResults').classList.remove('d-none');
            } else {
                uploadStatus.innerHTML = `<div class="alert alert-danger">Error: ${result.error}</div>`;
            }
        } catch (error) {
            uploadStatus.innerHTML = '<div class="alert alert-danger">Processing failed. Please try again.</div>';
            console.error('Upload error:', error);
        }
    });
});

function resetUI() {
    // Hide all result sections
    document.getElementById('extractedContent').classList.add('d-none');
    document.getElementById('processingOptions').classList.add('d-none');
    document.getElementById('processingResults').classList.add('d-none');
    document.getElementById('generatedQuestions').classList.add('d-none');
    document.getElementById('experienceAnalysis').classList.add('d-none');
    document.getElementById('skillGaps').classList.add('d-none');
    
    // Clear previous results
    document.getElementById('extractedText').textContent = '';
    document.getElementById('uploadStatus').innerHTML = '';
}

async function generateQuestions() {
    const questionsDiv = document.getElementById('generatedQuestions');
    questionsDiv.classList.remove('d-none');
    questionsDiv.querySelector('.card-body').innerHTML = '<div class="text-center">Generating questions...</div>';
    
    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'generate_questions',
                filename: currentFilename
            })
        });
        
        const result = await response.json();
        if (response.ok && result.questions) {
            questionsDiv.querySelector('.card-body').innerHTML = `
                <ul class="list-group">
                    ${result.questions.map(q => `
                        <li class="list-group-item">${q}</li>
                    `).join('')}
                </ul>
            `;
        }
    } catch (error) {
        questionsDiv.querySelector('.card-body').innerHTML = '<div class="alert alert-danger">Failed to generate questions.</div>';
    }
}

async function analyzeExperience() {
    const analysisDiv = document.getElementById('experienceAnalysis');
    analysisDiv.classList.remove('d-none');
    analysisDiv.querySelector('.card-body').innerHTML = '<div class="text-center">Analyzing experience...</div>';
    
    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'analyze_experience',
                filename: currentFilename
            })
        });
        
        const result = await response.json();
        if (response.ok && result.experience) {
            analysisDiv.querySelector('.card-body').innerHTML = `
                <pre class="bg-light p-3">${JSON.stringify(result.experience, null, 2)}</pre>
            `;
        }
    } catch (error) {
        analysisDiv.querySelector('.card-body').innerHTML = '<div class="alert alert-danger">Failed to analyze experience.</div>';
    }
}

function toggleTextView() {
    const extractedText = document.getElementById('extractedText');
    isRawView = !isRawView;
    
    if (isRawView) {
        extractedText.style.whiteSpace = 'pre-wrap';
    } else {
        extractedText.style.whiteSpace = 'normal';
    }
}