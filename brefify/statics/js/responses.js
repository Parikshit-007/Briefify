function getBotResponse(input) {
    //rock paper scissors
    if (input == "rock") {
        return "paper";
    } else if (input == "paper") {
        return "scissors";
    } else if (input == "scissors") {
        return "rock";
    }

    if (input == "how to generate summary") {
        return "log in, upload, generate. it's that easy!!";
    } else if (input == "what is this website") {
        return "This website allows you to upload long videos of lectures and converts them into short summary.";
    } else if (input == "scissors") {
        return "rock";
    }

    if (input == "tell me about website") {
        return "As remote and hybrid working models become more prevalent, virtual meetings have become necessary. Meetings are often held through platforms like Microsoft Teams, Google Meet, and Zoom. Although these platforms offer the ability to download transcripts, they cannot summarize them. In order to address this gap in meeting productivity, the project aims to create a solution that provides a summary of virtual meetings.";
    } else if (input == "tell me the objective of the website") {
        return "kaam karna lodu";
    } else if (input == "scissors") {
        return "rock";
    }



    // Simple responses
    if (input == "hello") {
        return "Hello there!";
    } else if (input == "goodbye") {
        return "Talk to you later!";
    } else {
        return "Try asking something else!";
    }
}