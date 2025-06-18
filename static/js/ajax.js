function getCSRFToken() {
    const regex = /csrftoken=([a-zA-Z0-9]*)/gm;
    const result = regex.exec(document.cookie);
    if (result.length > 0) {
        return result[1];
    } else {
        return null;
    }
}

function onLikeButtonClick(event) {
    const token = getCSRFToken();
    if (token) {
        const questionId = event.target.dataset.questionId;
        const answerId = event.target.dataset.answerId;
        const type = questionId ? 0 : 1;
        const id = questionId || answerId;
        const value = parseInt(event.target.dataset.value);

        const form = new FormData();
        form.append("type", type);
        form.append("id", id);
        form.append("value", value);
        form.append("csrfmiddlewaretoken", token);

        fetch("/make_like", {
            method: "POST",
            body: form,
        }).then(async (response) => {
            if (response.status == 200) {
                const data = await response.json();
                if (!data.error) {
                    const elementId = `${type === 0 ? "question" : "answer"}_${id}_likes`;
                    const likes = document.getElementById(elementId);
                    if (likes) {
                        likes.value = data.likes_count;
                    }
                }
            }
        }).catch(console.log);

    } else {
        window.location.replace("/login?continue=" + window.location.pathname);
    }
}

function onRightAnswerClick(event) {
    const token = getCSRFToken();
    if (token) {
        const question = event.target.dataset.questionId;
        const answer = event.target.dataset.answerId;

        const form = new FormData();
        form.append("question", question);
        form.append("answer", answer);
        form.append("csrfmiddlewaretoken", token);

        fetch("/question/right", {
            method: "POST",
            body: form,
        }).then(async (response) => {
            if (response.status == 200) {
                const data = await response.json();
                if (data.error) {
                    console.log("Error code:", data);
                }
            }
        }).catch(console.log);

    } else {
        window.location.replace("/login?continue=" + window.location.pathname);
    }
}