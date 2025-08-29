import streamlit as st
import requests
import base64
import json
from PIL import Image
import io
import uuid
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Calorie Estimation API Tester",
    page_icon="🍎",
    layout="wide"
)

# Main title
st.title("🍎 Calorie Estimation API Tester")
st.markdown("Upload an image of food to estimate its calorie content using the API")

# Sidebar for API configuration
st.sidebar.header("API Configuration")
api_base_url = st.sidebar.text_input(
    "API Base URL", 
    value="http://calorie_estimator:24000",
    help="Enter the base URL of your FastAPI server"
)
api_endpoint = "/api/predict"
full_url = f"{api_base_url}{api_endpoint}"
st.sidebar.text(f"Full endpoint: {full_url}")

# Function to convert image to base64
def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

# Function to call the API
def call_calorie_api(image_b64, request_id):
    """Call the calorie estimation API"""
    payload = {
        "request_id": request_id,
        "image": image_b64
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(full_url, json=payload, headers=headers, timeout=30)
        return response
    except requests.exceptions.RequestException as e:
        return None, str(e)

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Upload Image")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        help="Upload an image of food to estimate calories"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Image info
        st.write(f"**Image size:** {image.size}")
        st.write(f"**Image mode:** {image.mode}")
        st.write(f"**File size:** {uploaded_file.size} bytes")

with col2:
    st.header("API Response")
    
    if uploaded_file is not None:
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Show request details
        with st.expander("Request Details", expanded=False):
            st.write(f"**Request ID:** {request_id}")
            st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**API Endpoint:** {full_url}")
        
        # Predict button
        if st.button("🔍 Estimate Calories", type="primary", use_container_width=True):
            with st.spinner("Processing image..."):
                # Convert image to base64
                image_b64 = image_to_base64(image)
                
                # Call API
                response = call_calorie_api(image_b64, request_id)
                
                if isinstance(response, tuple):  # Error case
                    st.error(f"❌ Request failed: {response[1]}")
                elif response is not None:
                    # Display response
                    if response.status_code == 200:
                        try:
                            result = response.json()
                            st.success("✅ Prediction successful!")
                            
                            # Display results in a nice format
                            if isinstance(result, dict):
                                # Create metrics or formatted display based on your API response structure
                                st.subheader("Estimation Results")
                                
                                # Display the full JSON response
                                st.json(result)
                                
                            else:
                                st.write("**API Response:**")
                                st.write(result)
                                
                        except json.JSONDecodeError:
                            st.error("❌ Invalid JSON response from API")
                            st.code(response.text)
                    else:
                        st.error(f"❌ API Error (Status {response.status_code})")
                        try:
                            error_response = response.json()
                            st.json(error_response)
                        except:
                            st.code(response.text)
                else:
                    st.error("❌ Failed to connect to API")

# Additional features section
st.markdown("---")

# API Testing section
with st.expander("🔧 Advanced Testing Options", expanded=False):
    st.subheader("Manual API Testing")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Test with sample request:**")
        sample_request_id = st.text_input("Request ID", value=str(uuid.uuid4()))
        
        if st.button("Test API Health"):
            try:
                # Simple health check (you might want to add a health endpoint to your API)
                health_response = requests.get(f"{api_base_url}/docs", timeout=5)
                if health_response.status_code == 200:
                    st.success("✅ API is accessible")
                else:
                    st.warning(f"⚠️ API responded with status {health_response.status_code}")
            except:
                st.error("❌ Cannot reach API")
    
    with col2:
        st.write("**Response Format Expected:**")
        st.code("""
{
    "calories": 350,
    "food_items": ["apple", "banana"],
    "confidence": 0.85
}
        """, language="json")

# Instructions section
with st.expander("📖 How to Use", expanded=False):
    st.markdown("""
    ### Instructions:
    1. **Configure API**: Set your FastAPI server URL in the sidebar
    2. **Upload Image**: Choose a food image using the file uploader
    3. **Estimate Calories**: Click the "Estimate Calories" button
    4. **View Results**: See the API response with calorie estimation
    
    ### Supported Image Formats:
    - JPEG/JPG
    - PNG
    - BMP
    - TIFF
    
    ### Troubleshooting:
    - Ensure your FastAPI server is running
    - Check the API URL is correct
    - Make sure the image is clear and shows food items
    - Check the API logs if you encounter errors
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with Streamlit • Test your Calorie Estimation API"
    "</div>", 
    unsafe_allow_html=True
)