# Food Calorie Estimator App
## Objective
Design an AI-powered backend service that estimates calorie content from meal images using LLM-powered or vision-based tools. The focus is on **ingredient recognition**, **quantity estimation**, and **calorie computation**. This task evaluates your API design, AI pipeline structuring, and production-minded thinking.

## Features
Your solution should include:
- **Ingredient Recognition**: Detect ingredients from the image and estimate their quantities.
- **Calorie Estimation**: Calculate total calories using known nutritional information.
- **Confidence Score**: Indicate how confident the model is in its estimation.
- **Quality Handling**: If image quality is poor, return a helpful message and recommendation.

## Dataset Collection
There are some datasets that contain calories information to use:
- [Nutrition5k](https://github.com/google-research-datasets/Nutrition5k)  
- [NutritionVerse-Real](https://www.kaggle.com/datasets/nutritionverse/nutritionverse-real)  
- [SnapME](https://agdatacommons.nal.usda.gov/articles/dataset/SNAPMe_A_Benchmark_Dataset_of_Food_Photos_with_Food_Records_for_Evaluation_of_Computer_Vision_Algorithms_in_the_Context_of_Dietary_Assessment/24856449) - *preferred*
- [Recipe1M](https://pic2recipe.csail.mit.edu/) — *too large for the current stage, will ignore for now*

Here is my data preparation steps:
- I collect 3 data: Nutrition5k, NutritionVerse-Real and SnapME.
- Preprocess to get the metadata of each data including: `image_path`, `ingredients` (list) and `total_calories`.
- I picked up some images of each dataset to test because I don't have much tokens to run all of them.
- The final dataset can be download at [GoogleDrive](https://drive.google.com/file/d/1WSgHxYf7KOCipUSijXkTaj-m4et2i9HW/view?usp=sharing). 
- Some test examples are located in `tests/`. 

## Setup
#### Environment File
Create an `.env` file contain config in the format below:
```bash
MODEL_NAME=<model-to-use>   # openai or gemini
MODEL_ID=<model-id>         # version of the model: e.g. gpt-4o-mini, gemini-2.5-flash
MODEL_KEY=<model-api-key>   # api key
```
#### IMPORTANT NOTE:
- I provide both `Gemini` and `OpenAI` model wrapper.
- I used `Gemini`:`Gemini-Flash-2.5` by default.
- When I experimented my prompt in both `Gemini` and `ChatGPT` Web UI, I noticed that `GPT-5` usually estimated closer to the ground truth calories, `Gemini` sometimes overestimated the calories.
- If you have both `OpenAI` and `Gemini` key. I suggest you try both to test the performance.


#### Database Environment
- If you have **public host** MongoDB and want to save service log, add these to `.env` file:
```bash
DB_HOST=<mongo-db-host>
DB_PORT=<mongo-db-port>
DB_USERNAME=<mongo-db-username>
DB_PASSWORD=<mongo-db-password>
DB_AUTH=<mongo-db-auth-method>      # usually 'admin'
```

- If you run with **docker compose** add these to `.env` file:
```bash
DB_HOST=mongodb
DB_PORT=27017
DB_USERNAME=<mongo-db-username>
DB_PASSWORD=<mongo-db-password>
DB_AUTH=<mongo-db-auth-method>      # usually 'admin'
```

### Option 1: Docker Compose
#### IMPORTANT NOTE: 
- Check for available ports (27017, 24000 and 8501) before run the script. 
- If the port is not available, edit in the external mount port of `docker-compose.yaml` file.
- Make sure your `.env` file looks like this:
```bash
MODEL_NAME=<model-to-use>   # openai or gemini
MODEL_ID=<model-id>         # version of the model: e.g. gpt-5, gpt-4o-mini, gemini-2.5-flash,...
MODEL_KEY=<model-api-key>   # api key
DB_HOST=mongodb
DB_PORT=27017
DB_USERNAME=<mongo-db-username>
DB_PASSWORD=<mongo-db-password>
DB_AUTH=admin
```
#### Run: 
```bash
docker compose up -d --build
```

Shut down:
```bash
docker compose down -v
```
#### Access:
- `http://localhost:8501/`: UI.
- `http://localhost:24000/docs`: Documents swagger.
- `mongodb://<db-username>:<db-password>@localhost:27017/?authMechanism=DEFAULT`: Open with MongoDB Compass to see log.

### Option 2: Run Each Component
First you need to setup `MongoDB` service. Then build the `Calorie Estimator` image. Finally you can run the UI in folder `ui/`.
#### IMPORTANT NOTE:
- Be careful with network. If you run each component, I suggest use the flag `--net host` in `docker run` to run the services.  

#### Build
```bash
docker build . -t calorie-estimator-app
```
#### Run
```bash
docker run -it -d \
           --name calorie_estimator \
           --env-file .env \
           --privileged \
           -p 24000:24000 \ # Edit external port if you want
           calorie-estimator-app
```
#### Run UI
```bash
cd ui/
pip install requirements.txt
streamlit run app.py
```

## API Document
**NOTE**: Visit `http://localhost:24000/docs` to access **swagger**. 

### Predict API
- Type: `POST`
- Route: `/api/predict`
- Request data:
    - `request_id`: string
    - `image`: base64 image
- Example curl:
```bash
curl -X 'POST' \
  '<endpoint>/api/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "request_id": "<request_id>",
  "image": "data:image/jpeg;base64,/9j/.....<base64_image>"
}'
```
or
```bash
curl -X 'POST' \
  '<endpoint>/api/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "request_id": "<request_id>",
  "image": "/9j/.....<base64_image>"
}'
```

- Response format examples: 
```json
{
  "ingredients": [
    {
      "name": "pizza",
      "quantity": "3",
      "unit": "slice",
      "calories": 900,
      "calories_per_unit": 300 
    }
  ],
  "total_calories": 900,
  "confidence": 0.82,
  "recommendation": null
}
```
```json
{
  "ingredients": [],
  "total_calories": null,
  "confidence": 0.0,
  "recommendation": "Image too blurry. Please retake with better lighting and top-down angle."
}
```

## Server Benchmarking
To test the server workload capacity. Visit [Benchmark_README.md](benchmark/README.md).

## Discussions
- The response time: 5-7s
- The model can properly handle fail case. 
- Both the `gemini-2.5-flash` and `gpt-4o-mini` model can both estimate the calories for normal images, but trade-off between model at some cases.
- When `gemini-2.5-flash` and `gpt-4o-mini` mistakenly estimate the calories, both of them **overestimate**.
- I tested the `gpt-5` in Web UI with the same prompt, the model can estimate more closer to the ground truth.
- If you have redundant `OpenAI` and `Gemini` tokens. I suggest you try both to test the performance.

## Future Enhancement
### Re-Check Dataset 
Might double-check the dataset calories information for some meals.

### Benchmaark
Prepare dataset and design the benchmark process:
1. Collect image and prepare the metadata for each image contain at least `total_calories` information.
2. Design the metrics:
    - Calculate how many percentage the predicted calorie differ from the ground truth.
    - If that differences is lower than a threshold (5%, 10%, 15%, .etc) then consider the prediction is correct, else incorrect.
    - Calculate accuracy.

Use the metrics above to benchmark the model performance. 

### Chain of Prompts
We can try enhance the prompt with chain of prompts:
1. Collect and prepare a database of every ingredients and their corresponding calories. This can be done by crawling on public website or find public dataset.
2. Store the ingredients information: `name`, `calories` in a vector database.
3. When receive the image of the meal, design the prompt to guide the model to extract ingredients name, mass and units.
4. Query to database to get related information on their calories and add to the second prompt for the model to re-calculate the total calories.  

### ChatGPT God Mode?
Check for prompt like: `You are an expert in ...`. Example: [ChatGPT God Mode](https://www.linkedin.com/pulse/how-use-god-mode-chatgpt-unlocking-advanced-andreas-michaelides-phd-kavve/)

### ReAct
Following the paradigm of ReAct (Though, Action, Observation) to use external tools like Database Query or External Model. Example:
```
Thought 1: Tôi cần biết đây là món gì từ ảnh.
Action 1: ImageClassifier(photo.jpg) # Or ask the model to classify, instead of training new model
Observation 1: Phở bò.

Thought 2: Tôi cần tìm thành phần chính của phở bò.
Action 2: QueryNutritionDB("phở bò ingredients")
Observation 2: [bánh phở, thịt bò, nước dùng, rau]

Thought 3: Tôi cần biết khối lượng ước lượng trong ảnh.
Action 3: PortionEstimator(photo.jpg) # Or ask the model to estimate
Observation 3: 200g bánh phở, 100g thịt bò, 50ml nước dùng.

Thought 4: Tôi cần tính calo từ khối lượng và nutrition DB.
Action 4: QueryNutritionDB("200g bánh phở + 100g thịt bò + 50ml nước dùng")
Observation 4: 530 cal.

Thought 5: Giờ tôi có thể trả lời.
Final Answer: Khoảng 530 calories.
``` 