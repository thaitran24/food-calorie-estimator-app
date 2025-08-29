# Take-home Test: Calorie Estimation from Meal Images

## Objective
Design an AI-powered backend service that estimates calorie content from meal images using LLM-powered or vision-based tools. The focus is on **ingredient recognition**, **quantity estimation**, and **calorie computation**. This task evaluates your API design, AI pipeline structuring, and production-minded thinking.

## Features
Your solution should include:
- **Ingredient Recognition**: Detect ingredients from the image and estimate their quantities.
- **Calorie Estimation**: Calculate total calories using known nutritional information.
- **Confidence Score**: Indicate how confident the model is in its estimation.
- **Quality Handling**: If image quality is poor, return a helpful message and recommendation.

## Expected Output (JSON)

### If successful:
```json
{
  "ingredients": [
    { "name": "fried egg", "quantity": "1", "unit": "piece" },
    { "name": "white rice", "quantity": "1", "unit": "cup" }
  ],
  "total_calories": 420,
  "confidence": 0.86,
  "recommendation": null
}
```

### If image is poor quality:
```json
{
  "ingredients": [],
  "total_calories": null,
  "confidence": 0.0,
  "recommendation": "Image too blurry. Please retake with better lighting and top-down angle."
}
```

## Tooling Notes
You may use:
- **Vision models**: BLIP, Gemini Vision, CLIP, GPT-4o, etc.
- **Nutrition data**: OpenFoodFacts, USDA, or mocked data sources

## Deliverables
- `main.py` or `app.py`: CLI or API entrypoint
- `calorie_estimator/`: Core modules
- `tests/`: Basic test cases
- `requirements.txt`
- `README.md`: Setup, example usage, API explanation

## Evaluation Criteria

| Area | Points | Description |
|------|--------|-------------|
| Code Quality | 10 | Modular, readable, testable code |
| API & AI Logic | 10 | Accurate calorie estimate, clean structure |
| Production Maturity | 5 | Logging, error handling, no hardcoded values |
| Documentation | 5 | Clear setup, examples, instructions |

**Total: 30 points**

## Optional
- Streamlit or Gradio UI (optional)
- Use `.env` or config file for API keys