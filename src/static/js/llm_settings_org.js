// ----------------------------------------------------------------------------
// locations
const alertMsg = document.getElementById("alert-msg");

// functions
// use form for submit
const llmsettingsForm = document.getElementById("llm-settings-form");
llmsettingsForm.addEventListener("submit", function () {
    const form = $(this).closest("form");
    const status_message = form.attr("status_message");
    if (status_message) {
        alertMsg.innerHTML = "<div class='alert alert-success d-inline-flex' role='alert'>LLM settings set/updated</div>";
    } else {
        alertMsg.innerHTML = "<div class='alert alert-danger d-inline-flex' role='alert'>LLM not settings set/updated</div>";
    }
    // Remove error after 10 seconds
    setTimeout(() => alertMsg.remove(), 20000);
});


// ----------------------------------------------------------------------------
// Dropdown with no function
const llmList = ['openai', 'llama2', 'huggingface'];
// llm category
let llmOptions = "<option value=''>Select LLM Option</option>"
    + llmList.map(llm =>
        `<option value='${llm}'>${llm}</option>`).join('\n');
console.log(llmOptions);
document.getElementById("id_llm").innerHTML = llmOptions;


// ----------------------------------------------------------------------------
// Dropdown with no function
const vectorList = ['chroma', 'faiss', 'pinecone', 'pgvector', 'weaviate', 'sklearnvectorstore'];
// vector category
let vectorOptions = "<option value=''>Select Vector Option</option>"
    + vectorList.map(vector =>
        `<option value='${vector}'>${vector}</option>`).join('\n');
console.log(vectorOptions);
document.getElementById("id_vector_db").innerHTML = vectorOptions;
