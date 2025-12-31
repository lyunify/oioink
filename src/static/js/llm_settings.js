// ----------------------------------------------------------------------------
// locations
const alertMsg = document.getElementById("alert-msg");

// functions
// use form for submit
const llmsettingsForm = document.getElementById("llm-settings-form");
llmsettingsForm.addEventListener("submit", function () {
    const form = $(this).closest("form");
    const status_message = form.attr("status_message");
    //if (status_message) {
    //    alertMsg.innerHTML = "<div class='alert alert-success d-inline-flex' role='alert'>LLM settings set/updated</div>";
    //} else {
    //    alertMsg.innerHTML = "<div class='alert alert-danger d-inline-flex' role='alert'>LLM not settings set/updated</div>";
    //}
    // Remove error after 10 seconds
    alertMsg.innerHTML = "<div class='alert alert-success d-inline-flex' role='alert'>LLM settings set/updated</div>";
    setTimeout(() => alertMsg.remove(), 20000);
});


// ----------------------------------------------------------------------------
// llm - dropdown with no function
const llmList = ['openai', 'huggingface'];
// llm category
let llmOptions = "<option value=''>Select LLM Option</option>"
    + llmList.map(llm =>
        `<option value='${llm}'>${llm}</option>`).join('\n');
console.log(llmOptions);
document.getElementById("id_llm").innerHTML = llmOptions;

// llm model - dropdown with no function
const llmModelList =
    ['openai gpt-3.5-turbo',
        'openai gpt-3.5-turbo-16k',
        'openai gpt-3.5-turbo-instruct',
        'openai gpt-3.5-turbo-0613',
        'openai gpt-3.5-turbo-16k-0613',
        'huggingface llama2'];
// llm model category
let llmModelOptions = "<option value=''>Select LLM Model Option</option>"
    + llmModelList.map(llm_model =>
        `<option value='${llm_model}'>${llm_model}</option>`).join('\n');
console.log(llmModelOptions);
document.getElementById("id_llm_model").innerHTML = llmModelOptions;

// llm temperature - dropdown with no function
const llmTemperatureList = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5];
// llm temperature category
let llmTemperatureOptions = "<option value=''>Select LLM Temperature Option</option>"
    + llmTemperatureList.map(llm_temperature =>
        `<option value='${llm_temperature}'>${llm_temperature}</option>`).join('\n');
console.log(llmTemperatureOptions);
document.getElementById("id_llm_temperature").innerHTML = llmTemperatureOptions;


// ----------------------------------------------------------------------------
// vector db - dropdown with no function
const vectorList = ['chroma', 'faiss', 'pinecone', 'pgvector', 'weaviate', 'sklearnvectorstore'];
// vector category
let vectorOptions = "<option value=''>Select Vector Option</option>"
    + vectorList.map(vector =>
        `<option value='${vector}'>${vector}</option>`).join('\n');
console.log(vectorOptions);
document.getElementById("id_vector_db").innerHTML = vectorOptions;
