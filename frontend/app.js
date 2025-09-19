// Career Guidance System JavaScript

// Data from the provided JSON
const riasecQuestions = [
    {"id": 1, "text": "I enjoy working with my hands and building things", "type": "R"},
    {"id": 2, "text": "I like to analyze data and solve complex problems", "type": "I"},
    {"id": 3, "text": "I enjoy creating art, writing, or other creative works", "type": "A"},
    {"id": 4, "text": "I like helping and teaching other people", "type": "S"},
    {"id": 5, "text": "I enjoy leading teams and making business decisions", "type": "E"},
    {"id": 6, "text": "I prefer organized, detailed work with clear procedures", "type": "C"},
    {"id": 7, "text": "I like working with tools, machines, or equipment", "type": "R"},
    {"id": 8, "text": "I enjoy conducting research and experiments", "type": "I"},
    {"id": 9, "text": "I like to express myself through creative mediums", "type": "A"},
    {"id": 10, "text": "I enjoy counseling and guiding others", "type": "S"},
    {"id": 11, "text": "I like to persuade and influence people", "type": "E"},
    {"id": 12, "text": "I prefer working with numbers and data organization", "type": "C"},
    {"id": 13, "text": "I enjoy outdoor activities and physical work", "type": "R"},
    {"id": 14, "text": "I like to study and understand how things work", "type": "I"},
    {"id": 15, "text": "I enjoy music, drama, or visual arts", "type": "A"},
    {"id": 16, "text": "I like to work in teams and collaborate with others", "type": "S"},
    {"id": 17, "text": "I enjoy taking risks and starting new ventures", "type": "E"},
    {"id": 18, "text": "I prefer structured environments with clear rules", "type": "C"},
    {"id": 19, "text": "I like mechanical and technical activities", "type": "R"},
    {"id": 20, "text": "I enjoy reading scientific journals and research", "type": "I"},
    {"id": 21, "text": "I like to design and create original works", "type": "A"},
    {"id": 22, "text": "I enjoy community service and helping others", "type": "S"},
    {"id": 23, "text": "I like to manage and organize people or projects", "type": "E"},
    {"id": 24, "text": "I prefer routine tasks and systematic approaches", "type": "C"},
    {"id": 25, "text": "I enjoy working with animals or plants", "type": "R"},
    {"id": 26, "text": "I like to investigate and solve mysteries", "type": "I"},
    {"id": 27, "text": "I enjoy storytelling and creative writing", "type": "A"},
    {"id": 28, "text": "I like to train and develop others", "type": "S"},
    {"id": 29, "text": "I enjoy networking and making business connections", "type": "E"},
    {"id": 30, "text": "I prefer detailed record-keeping and documentation", "type": "C"}
];

const personalityTypes = {
    "R": {
        "name": "Realistic",
        "description": "Hands-on, practical work with tools, machines, or outdoors",
        "careers": ["Engineer", "Mechanic", "Farmer", "Carpenter", "Pilot"],
        "color": "#ef4444"
    },
    "I": {
        "name": "Investigative", 
        "description": "Research, analysis, and scientific work",
        "careers": ["Scientist", "Researcher", "Doctor", "Analyst", "Professor"],
        "color": "#3b82f6"
    },
    "A": {
        "name": "Artistic",
        "description": "Creative expression and original thinking",
        "careers": ["Artist", "Designer", "Writer", "Musician", "Actor"],
        "color": "#8b5cf6"
    },
    "S": {
        "name": "Social",
        "description": "Helping, teaching, and working with people",
        "careers": ["Teacher", "Counselor", "Social Worker", "Nurse", "Trainer"],
        "color": "#10b981"
    },
    "E": {
        "name": "Enterprising",
        "description": "Leadership, business, and persuading others",
        "careers": ["Manager", "Entrepreneur", "Sales Rep", "Lawyer", "Executive"],
        "color": "#f59e0b"
    },
    "C": {
        "name": "Conventional",
        "description": "Organization, detail work, and structured tasks",
        "careers": ["Accountant", "Administrator", "Banker", "Secretary", "Clerk"],
        "color": "#6b7280"
    }
};

const colleges = [
    {"name": "University of Kashmir", "location": "Srinagar", "type": "University", "courses": ["Engineering", "Medicine", "Arts", "Science"]},
    {"name": "NIT Srinagar", "location": "Srinagar", "type": "Technical", "courses": ["Engineering", "Technology"]},
    {"name": "Government Medical College Srinagar", "location": "Srinagar", "type": "Medical", "courses": ["Medicine", "Nursing"]},
    {"name": "University of Jammu", "location": "Jammu", "type": "University", "courses": ["Engineering", "Management", "Arts"]},
    {"name": "Jammu University", "location": "Jammu", "type": "University", "courses": ["Science", "Commerce", "Arts"]},
    {"name": "Islamic University of Science and Technology", "location": "Awantipora", "type": "University", "courses": ["Engineering", "Medicine", "Management"]},
    {"name": "Cluster University Srinagar", "location": "Srinagar", "type": "University", "courses": ["Arts", "Science", "Commerce"]},
    {"name": "Baba Ghulam Shah Badshah University", "location": "Rajouri", "type": "University", "courses": ["Arts", "Science", "Education"]},
    {"name": "Sher-e-Kashmir University of Agricultural Sciences", "location": "Srinagar", "type": "University", "courses": ["Agriculture", "Veterinary", "Forestry"]},
    {"name": "Central University of Kashmir", "location": "Ganderbal", "type": "University", "courses": ["Science", "Arts", "Management"]}
];

const sampleResults = {
    "name": "Sample Student",
    "scores": {"R": 85, "I": 92, "A": 78, "S": 65, "E": 71, "C": 58},
    "primaryType": "I",
    "secondaryType": "R",
    "recommendedCareers": ["Research Scientist", "Data Analyst", "Software Engineer", "Biomedical Engineer"],
    "recommendedCourses": ["Computer Science", "Biotechnology", "Data Science", "Research & Development"]
};

// Global state
let currentAssessment = {
    userName: '',
    currentQuestionIndex: 0,
    responses: {},
    isCompleted: false
};

let assessmentResults = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupNavigation();
    setupActionCards();
    setupAssessment();
    setupColleges();
    setupResults();
});

// Navigation Setup - Fixed version
function setupNavigation() {
    // Use event delegation for better reliability
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('nav-btn') || e.target.closest('.nav-btn')) {
            const button = e.target.classList.contains('nav-btn') ? e.target : e.target.closest('.nav-btn');
            const targetSection = button.getAttribute('data-section');
            
            if (targetSection) {
                showSection(targetSection);
                updateActiveNavButton(button);
            }
        }
    });
}

function showSection(sectionId) {
    // Hide all sections
    const allSections = document.querySelectorAll('.section');
    allSections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
}

function updateActiveNavButton(activeButton) {
    // Remove active class from all nav buttons
    const allNavButtons = document.querySelectorAll('.nav-btn');
    allNavButtons.forEach(btn => btn.classList.remove('active'));
    
    // Add active class to clicked button
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

// Action Cards Setup
function setupActionCards() {
    document.addEventListener('click', function(e) {
        // Handle action cards
        if (e.target.closest('.action-card')) {
            const card = e.target.closest('.action-card');
            const action = card.getAttribute('data-action');
            if (action) {
                handleActionCard(action);
            }
        }
        
        // Handle action buttons
        if (e.target.hasAttribute('data-action')) {
            const action = e.target.getAttribute('data-action');
            handleActionCard(action);
        }
    });
}

function handleActionCard(action) {
    switch(action) {
        case 'take-assessment':
            showSection('assessment');
            updateActiveNavButton(document.querySelector('[data-section="assessment"]'));
            break;
        case 'browse-colleges':
            showSection('colleges');
            updateActiveNavButton(document.querySelector('[data-section="colleges"]'));
            break;
        case 'learn-riasec':
            showSection('about');
            updateActiveNavButton(document.querySelector('[data-section="about"]'));
            break;
        case 'sample-results':
            displayResults(sampleResults);
            showSection('results');
            updateActiveNavButton(document.querySelector('[data-section="results"]'));
            break;
    }
}

// Assessment Setup
function setupAssessment() {
    document.addEventListener('click', function(e) {
        if (e.target.id === 'startAssessment') {
            startAssessment();
        } else if (e.target.id === 'prevQuestion') {
            previousQuestion();
        } else if (e.target.id === 'nextQuestion') {
            nextQuestion();
        } else if (e.target.id === 'finishAssessment') {
            finishAssessment();
        } else if (e.target.classList.contains('rating-btn')) {
            selectRating(e.target.getAttribute('data-rating'));
        }
    });

    // Reset assessment when entering section
    document.addEventListener('click', function(e) {
        if (e.target.getAttribute('data-section') === 'assessment' && currentAssessment.isCompleted) {
            resetAssessment();
        }
    });
}

function startAssessment() {
    const userName = document.getElementById('userName').value.trim();
    
    if (!userName) {
        alert('Please enter your name to begin the assessment.');
        return;
    }

    currentAssessment.userName = userName;
    currentAssessment.currentQuestionIndex = 0;
    currentAssessment.responses = {};
    currentAssessment.isCompleted = false;

    document.getElementById('assessmentStart').classList.add('hidden');
    document.getElementById('assessmentQuestions').classList.remove('hidden');

    displayQuestion();
}

function displayQuestion() {
    const question = riasecQuestions[currentAssessment.currentQuestionIndex];
    const questionText = document.getElementById('questionText');
    const questionCounter = document.getElementById('questionCounter');
    const prevBtn = document.getElementById('prevQuestion');
    const nextBtn = document.getElementById('nextQuestion');
    const finishBtn = document.getElementById('finishAssessment');

    questionText.textContent = question.text;
    questionCounter.textContent = `Question ${currentAssessment.currentQuestionIndex + 1} of ${riasecQuestions.length}`;

    // Update button states
    prevBtn.disabled = currentAssessment.currentQuestionIndex === 0;
    
    const isLastQuestion = currentAssessment.currentQuestionIndex === riasecQuestions.length - 1;
    nextBtn.classList.toggle('hidden', isLastQuestion);
    finishBtn.classList.toggle('hidden', !isLastQuestion);

    // Clear previous rating selection
    document.querySelectorAll('.rating-btn').forEach(btn => btn.classList.remove('selected'));

    // Show current rating if exists
    const currentResponse = currentAssessment.responses[question.id];
    if (currentResponse) {
        const selectedBtn = document.querySelector(`[data-rating="${currentResponse}"]`);
        if (selectedBtn) {
            selectedBtn.classList.add('selected');
        }
        nextBtn.disabled = false;
        finishBtn.disabled = false;
    } else {
        nextBtn.disabled = true;
        finishBtn.disabled = true;
    }

    updateProgress();
}

function selectRating(rating) {
    const question = riasecQuestions[currentAssessment.currentQuestionIndex];
    currentAssessment.responses[question.id] = parseInt(rating);

    // Update UI
    document.querySelectorAll('.rating-btn').forEach(btn => btn.classList.remove('selected'));
    document.querySelector(`[data-rating="${rating}"]`).classList.add('selected');

    // Enable next/finish button
    document.getElementById('nextQuestion').disabled = false;
    document.getElementById('finishAssessment').disabled = false;
}

function previousQuestion() {
    if (currentAssessment.currentQuestionIndex > 0) {
        currentAssessment.currentQuestionIndex--;
        displayQuestion();
    }
}

function nextQuestion() {
    if (currentAssessment.currentQuestionIndex < riasecQuestions.length - 1) {
        currentAssessment.currentQuestionIndex++;
        displayQuestion();
    }
}

function updateProgress() {
    const progress = ((currentAssessment.currentQuestionIndex + 1) / riasecQuestions.length) * 100;
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');

    progressFill.style.width = `${progress}%`;
    progressText.textContent = `${currentAssessment.currentQuestionIndex + 1}/${riasecQuestions.length}`;
}

function finishAssessment() {
    // Check if all questions are answered
    const totalQuestions = riasecQuestions.length;
    const answeredQuestions = Object.keys(currentAssessment.responses).length;

    if (answeredQuestions < totalQuestions) {
        alert('Please answer all questions before finishing the assessment.');
        return;
    }

    // Calculate results
    assessmentResults = calculateResults();
    currentAssessment.isCompleted = true;

    // Display results
    displayResults(assessmentResults);
    showSection('results');
    updateActiveNavButton(document.querySelector('[data-section="results"]'));
}

function calculateResults() {
    const scores = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 };
    const maxPossibleScore = 5 * 5; // 5 questions per type * 5 max rating

    // Sum up scores for each type
    riasecQuestions.forEach(question => {
        const response = currentAssessment.responses[question.id];
        if (response) {
            scores[question.type] += response;
        }
    });

    // Convert to percentages
    Object.keys(scores).forEach(type => {
        scores[type] = Math.round((scores[type] / maxPossibleScore) * 100);
    });

    // Find primary and secondary types
    const sortedTypes = Object.entries(scores).sort((a, b) => b[1] - a[1]);
    const primaryType = sortedTypes[0][0];
    const secondaryType = sortedTypes[1][0];

    // Generate career recommendations
    const recommendedCareers = [
        ...personalityTypes[primaryType].careers.slice(0, 3),
        ...personalityTypes[secondaryType].careers.slice(0, 2)
    ];

    return {
        name: currentAssessment.userName,
        scores: scores,
        primaryType: primaryType,
        secondaryType: secondaryType,
        recommendedCareers: recommendedCareers,
        recommendedCourses: generateCourseRecommendations(primaryType, secondaryType)
    };
}

function generateCourseRecommendations(primary, secondary) {
    const courseMapping = {
        R: ["Engineering", "Technology", "Agriculture"],
        I: ["Science", "Medicine", "Research & Development"],
        A: ["Arts", "Design", "Creative Writing"],
        S: ["Education", "Social Work", "Psychology"],
        E: ["Management", "Business Administration", "Commerce"],
        C: ["Accounting", "Administration", "Data Management"]
    };

    return [
        ...courseMapping[primary].slice(0, 2),
        ...courseMapping[secondary].slice(0, 2)
    ];
}

function resetAssessment() {
    currentAssessment = {
        userName: '',
        currentQuestionIndex: 0,
        responses: {},
        isCompleted: false
    };

    document.getElementById('userName').value = '';
    document.getElementById('assessmentStart').classList.remove('hidden');
    document.getElementById('assessmentQuestions').classList.add('hidden');
    
    // Reset progress
    document.getElementById('progressFill').style.width = '0%';
    document.getElementById('progressText').textContent = '0/30';
}

// Colleges Setup
function setupColleges() {
    displayColleges(colleges);
    
    document.addEventListener('change', function(e) {
        if (e.target.id === 'collegeFilter') {
            const filterValue = e.target.value;
            const filteredColleges = filterValue === 'all' ? 
                colleges : 
                colleges.filter(college => college.type === filterValue);
            displayColleges(filteredColleges);
        }
    });
}

function displayColleges(collegeList) {
    const grid = document.getElementById('collegesGrid');
    
    grid.innerHTML = collegeList.map(college => `
        <div class="college-card">
            <div class="college-name">${college.name}</div>
            <div class="college-location">
                <i class="fas fa-map-marker-alt"></i> ${college.location}
            </div>
            <div class="college-type">${college.type}</div>
            <div class="college-courses">
                <strong>Courses:</strong> ${college.courses.join(', ')}
            </div>
        </div>
    `).join('');
}

// Results Setup
function setupResults() {
    document.addEventListener('click', function(e) {
        if (e.target.id === 'exportResults') {
            exportResults();
        } else if (e.target.id === 'retakeAssessment') {
            resetAssessment();
            showSection('assessment');
            updateActiveNavButton(document.querySelector('[data-section="assessment"]'));
        }
    });
}

function displayResults(results) {
    const placeholder = document.getElementById('resultsPlaceholder');
    const content = document.getElementById('resultsContent');

    placeholder.classList.add('hidden');
    content.classList.remove('hidden');

    // Display personality chart
    createPersonalityChart(results.scores);

    // Display top types
    displayTopTypes(results);

    // Display recommended careers
    displayRecommendedCareers(results.recommendedCareers);

    // Display matching colleges
    displayMatchingColleges(results);
}

function createPersonalityChart(scores) {
    const ctx = document.getElementById('personalityChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.personalityChartInstance) {
        window.personalityChartInstance.destroy();
    }

    const chartData = {
        labels: Object.keys(scores).map(type => personalityTypes[type].name),
        datasets: [{
            label: 'Personality Scores',
            data: Object.values(scores),
            backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545'],
            borderColor: 'rgba(255, 255, 255, 0.8)',
            borderWidth: 2
        }]
    };

    window.personalityChartInstance = new Chart(ctx, {
        type: 'radar',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    },
                    pointLabels: {
                        color: 'rgba(255, 255, 255, 0.9)',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function displayTopTypes(results) {
    const container = document.getElementById('topTypes');
    const sortedScores = Object.entries(results.scores).sort((a, b) => b[1] - a[1]);
    
    container.innerHTML = sortedScores.slice(0, 3).map(([type, score]) => `
        <div class="type-result" style="margin-bottom: 16px; padding: 12px; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
            <div class="type-header" style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div class="type-indicator" style="background-color: ${personalityTypes[type].color}; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                    ${type}
                </div>
                <div>
                    <h4 style="margin: 0; color: white;">${personalityTypes[type].name}</h4>
                    <div class="score" style="color: rgba(255, 255, 255, 0.8); font-size: 14px;">${score}%</div>
                </div>
            </div>
            <p style="margin: 0; color: rgba(255, 255, 255, 0.7); font-size: 14px;">${personalityTypes[type].description}</p>
        </div>
    `).join('');
}

function displayRecommendedCareers(careers) {
    const container = document.getElementById('recommendedCareers');
    
    container.innerHTML = `
        <ul class="career-list" style="list-style: none; padding: 0; margin: 0;">
            ${careers.map(career => `<li class="career-item" style="padding: 8px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.9);">• ${career}</li>`).join('')}
        </ul>
    `;
}

function displayMatchingColleges(results) {
    const container = document.getElementById('matchingColleges');
    
    // Filter colleges based on recommended courses
    const matchingColleges = colleges.filter(college => 
        results.recommendedCourses.some(course => 
            college.courses.some(collegeCourse => 
                collegeCourse.toLowerCase().includes(course.toLowerCase()) ||
                course.toLowerCase().includes(collegeCourse.toLowerCase())
            )
        )
    );

    if (matchingColleges.length > 0) {
        container.innerHTML = matchingColleges.slice(0, 3).map(college => `
            <div class="matching-college" style="margin-bottom: 12px; padding: 12px; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                <strong style="color: white;">${college.name}</strong><br>
                <small style="color: rgba(255, 255, 255, 0.7);">${college.location} • ${college.type}</small>
            </div>
        `).join('');
    } else {
        container.innerHTML = '<p style="color: rgba(255, 255, 255, 0.8);">No specific matches found. Consider exploring all available colleges.</p>';
    }
}

function exportResults() {
    if (!assessmentResults) {
        alert('No results to export. Please complete the assessment first.');
        return;
    }

    const resultText = `
RIASEC Career Assessment Results
================================

Name: ${assessmentResults.name}
Assessment Date: ${new Date().toLocaleDateString()}

Personality Scores:
${Object.entries(assessmentResults.scores)
    .map(([type, score]) => `${personalityTypes[type].name} (${type}): ${score}%`)
    .join('\n')}

Primary Type: ${personalityTypes[assessmentResults.primaryType].name}
Secondary Type: ${personalityTypes[assessmentResults.secondaryType].name}

Recommended Careers:
${assessmentResults.recommendedCareers.map(career => `• ${career}`).join('\n')}

Recommended Courses:
${assessmentResults.recommendedCourses.map(course => `• ${course}`).join('\n')}

Generated by CareerGuide AI
    `.trim();

    const blob = new Blob([resultText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `RIASEC_Results_${assessmentResults.name.replace(/\s+/g, '_')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}