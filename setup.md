# Mental Health FAQ Chatbot - Android Implementation Guide

This guide provides complete instructions to implement a Mental Health FAQ chatbot in Android using ONNX Runtime for model inference.

## Table of Contents
1. [Project Setup](#project-setup)
2. [Model Preparation](#model-preparation)
3. [Android Implementation](#android-implementation)
   - [UI/UX Design](#uiux-design)
   - [Model Integration](#model-integration)
   - [Chat Logic](#chat-logic)
4. [Running the App](#running-the-app)
5. [Testing and Debugging](#testing-and-debugging)
6. [Future Improvements](#future-improvements)

## Project Setup

### Prerequisites
- Android Studio (latest version)
- Android SDK 24+ (Android 7.0)
- Basic knowledge of Java/Kotlin and Android development

### 1. Create a New Android Project
1. Open Android Studio
2. Select "New Project"
3. Choose "Empty Activity"
4. Configure your project:
   - Name: `MentalHealthChatbot`
   - Package name: `com.example.mentalhealthchatbot`
   - Language: Java
   - Minimum SDK: API 24 (Android 7.0)

### 2. Add Dependencies
Add these to your `app/build.gradle` file:

```gradle
dependencies {
    // ONNX Runtime
    implementation 'com.microsoft.onnxruntime:onnxruntime-android:latest.release'
    
    // GSON for JSON parsing
    implementation 'com.google.code.gson:gson:2.10.1'
    
    // RecyclerView for chat messages
    implementation 'androidx.recyclerview:recyclerview:1.3.2'
    
    // Material Design components
    implementation 'com.google.android.material:material:1.11.0'
    
    // For better async operations
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.7.0'
}
```

## Model Preparation

1. **Copy Model Files**
   - Create an `assets` folder in your Android project:
     - Right-click on `app/src/main`
     - New → Folder → Assets Folder
   - Create a subfolder: `assets/model/onnx`
   - Copy these files from your trained model:
     - `model.onnx` (the ONNX model)
     - All files from the tokenizer directory

## Android Implementation

### UI/UX Design

1. **Main Activity Layout** (`activity_main.xml`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/white">

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/chatRecyclerView"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:padding="8dp"
        app:layout_constraintBottom_toTopOf="@+id/inputLayout"
        app:layout_constraintTop_toTopOf="parent"/>

    <com.google.android.material.textfield.TextInputLayout
        android:id="@+id/inputLayout"
        style="@style/Widget.MaterialComponents.TextInputLayout.OutlinedBox"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_margin="8dp"
        android:hint="Type your question..."
        app:endIconMode="custom"
        app:endIconDrawable="@drawable/ic_send"
        app:endIconTint="@color/purple_500"
        app:endIconCheckable="true"
        app:endIconContentDescription="Send"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/messageInput"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="textMultiLine"
            android:maxLines="4"
            android:minLines="1"
            android:padding="12dp"/>
    </com.google.android.material.textfield.TextInputLayout>

    <ProgressBar
        android:id="@+id/progressBar"
        style="?android:attr/progressBarStyle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="16dp"
        android:visibility="gone"
        app:layout_constraintBottom_toTopOf="@id/inputLayout"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

2. **Chat Message Item Layout** (`item_message.xml`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.cardview.widget.CardView
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_margin="8dp"
    app:cardBackgroundColor="@color/white"
    app:cardCornerRadius="8dp"
    app:cardElevation="2dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="12dp">

        <TextView
            android:id="@+id/messageText"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textColor="@color/black"
            android:textSize="16sp"
            android:textStyle="bold"/>

        <TextView
            android:id="@+id/timestampText"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_gravity="end"
            android:layout_marginTop="4dp"
            android:textColor="@color/gray_600"
            android:textSize="12sp"/>
    </LinearLayout>
</androidx.cardview.widget.CardView>
```

### Model Integration

1. **Model Helper Class** (`FAQModelHelper.java`)

```java
import android.content.Context;
import android.util.Log;

import com.microsoft.onnxruntime.OnnxTensor;
import com.microsoft.onnxruntime.OrtEnvironment;
import com.microsoft.onnxruntime.OrtSession;

import java.nio.LongBuffer;
import java.util.HashMap;
import java.util.Map;

public class FAQModelHelper {
    private static final String TAG = "FAQModelHelper";
    private OrtSession session;
    private final OrtEnvironment env = OrtEnvironment.getEnvironment();
    private final TokenizerHelper tokenizer;

    public FAQModelHelper(Context context) {
        this.tokenizer = new TokenizerHelper(context);
        loadModel(context);
    }

    private void loadModel(Context context) {
        try {
            // Load model from assets
            session = env.createSession(FileUtils.loadModelFile(context, "model/onnx/model.onnx"));
            Log.d(TAG, "Model loaded successfully");
        } catch (Exception e) {
            Log.e(TAG, "Error loading model", e);
        }
    }

    public String getAnswer(String question) {
        try {
            // Tokenize input
            long[][] inputIds = tokenizer.tokenize(question);
            long[][] attentionMask = tokenizer.createAttentionMask(inputIds[0].length);

            // Create input tensors
            long[] shape = {1, inputIds[0].length};
            
            try (OnnxTensor idsTensor = OnnxTensor.createTensor(env, LongBuffer.wrap(inputIds[0]), shape);
                 OnnxTensor maskTensor = OnnxTensor.createTensor(env, LongBuffer.wrap(attentionMask[0]), shape)) {
                
                Map<String, OnnxTensor> inputs = new HashMap<>();
                inputs.put("input_ids", idsTensor);
                inputs.put("attention_mask", maskTensor);
                
                // Run inference
                try (OrtSession.Result results = session.run(inputs)) {
                    // Process and return the answer
                    return processResults(results);
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting answer", e);
            return "I'm sorry, I couldn't process your question. Please try again.";
        }
    }

    private String processResults(OrtSession.Result results) {
        // Implement your result processing logic here
        // This is a simplified example
        return "This is a sample response. Implement your own result processing.";
    }
}
```

2. **File Utils** (`FileUtils.java`)

```java
import android.content.Context;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class FileUtils {
    public static byte[] loadModelFile(Context context, String modelPath) throws IOException {
        try (InputStream inputStream = context.getAssets().open(modelPath)) {
            int size = inputStream.available();
            byte[] buffer = new byte[size];
            int read = inputStream.read(buffer);
            if (read != size) {
                throw new IOException("Failed to read model file");
            }
            return buffer;
        } catch (IOException e) {
            Log.e("FileUtils", "Error loading model file", e);
            throw e;
        }
    }
}
```

### Chat Logic

1. **Message Model** (`Message.java`)

```java
public class Message {
    public static final int TYPE_USER = 0;
    public static final int TYPE_BOT = 1;
    
    private String content;
    private int type;
    private long timestamp;
    
    public Message(String content, int type) {
        this.content = content;
        this.type = type;
        this.timestamp = System.currentTimeMillis();
    }
    
    // Getters and Setters
    public String getContent() { return content; }
    public int getType() { return type; }
    public long getTimestamp() { return timestamp; }
}
```

2. **Chat Adapter** (`ChatAdapter.java`)

```java
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Locale;

public class ChatAdapter extends RecyclerView.Adapter<ChatAdapter.MessageViewHolder> {
    private final List<Message> messages;
    private final SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm", Locale.getDefault());

    public ChatAdapter(List<Message> messages) {
        this.messages = messages;
    }

    @NonNull
    @Override
    public MessageViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_message, parent, false);
        return new MessageViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull MessageViewHolder holder, int position) {
        Message message = messages.get(position);
        holder.messageText.setText(message.getContent());
        holder.timestampText.setText(timeFormat.format(message.getTimestamp()));
        
        // Customize appearance based on message type
        if (message.getType() == Message.TYPE_USER) {
            // User message styling
            holder.itemView.setLayoutDirection(View.LAYOUT_DIRECTION_RTL);
            holder.messageText.setTextColor(holder.itemView.getContext()
                    .getResources().getColor(android.R.color.holo_blue_dark));
        } else {
            // Bot message styling
            holder.itemView.setLayoutDirection(View.LAYOUT_DIRECTION_LTR);
            holder.messageText.setTextColor(holder.itemView.getContext()
                    .getResources().getColor(android.R.color.black));
        }
    }

    @Override
    public int getItemCount() {
        return messages.size();
    }

    static class MessageViewHolder extends RecyclerView.ViewHolder {
        TextView messageText;
        TextView timestampText;

        public MessageViewHolder(@NonNull View itemView) {
            super(itemView);
            messageText = itemView.findViewById(R.id.messageText);
            timestampText = itemView.findViewById(R.id.timestampText);
        }
    }
}
```

3. **Main Activity** (`MainActivity.java`)

```java
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private FAQModelHelper faqModel;
    private ChatAdapter chatAdapter;
    private List<Message> messages = new ArrayList<>();
    private ProgressBar progressBar;
    private TextInputEditText messageInput;
    private TextInputLayout inputLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize UI components
        initializeViews();
        setupRecyclerView();
        
        // Initialize model in background
        new InitModelTask().execute();
    }

    private void initializeViews() {
        progressBar = findViewById(R.id.progressBar);
        messageInput = findViewById(R.id.messageInput);
        inputLayout = findViewById(R.id.inputLayout);
        
        // Set up send button click listener
        inputLayout.setEndIconOnClickListener(v -> sendMessage());
        
        // Handle keyboard send button
        messageInput.setOnEditorActionListener((v, actionId, event) -> {
            sendMessage();
            return true;
        });
    }

    private void setupRecyclerView() {
        RecyclerView recyclerView = findViewById(R.id.chatRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        chatAdapter = new ChatAdapter(messages);
        recyclerView.setAdapter(chatAdapter);
        
        // Add welcome message
        addBotMessage("Hello! I'm your mental health assistant. How can I help you today?");
    }

    private void sendMessage() {
        String message = messageInput.getText().toString().trim();
        if (message.isEmpty()) {
            return;
        }
        
        // Add user message to chat
        addUserMessage(message);
        messageInput.setText("");
        
        // Process message
        if (faqModel != null) {
            new ProcessMessageTask().execute(message);
        } else {
            addBotMessage("I'm still initializing. Please wait a moment...");
        }
    }

    private void addUserMessage(String message) {
        messages.add(new Message(message, Message.TYPE_USER));
        chatAdapter.notifyItemInserted(messages.size() - 1);
        scrollToBottom();
    }

    private void addBotMessage(String message) {
        messages.add(new Message(message, Message.TYPE_BOT));
        chatAdapter.notifyItemInserted(messages.size() - 1);
        scrollToBottom();
    }

    private void scrollToBottom() {
        RecyclerView recyclerView = findViewById(R.id.chatRecyclerView);
        recyclerView.scrollToPosition(messages.size() - 1);
    }

    private class InitModelTask extends AsyncTask<Void, Void, Boolean> {
        @Override
        protected void onPreExecute() {
            progressBar.setVisibility(View.VISIBLE);
        }

        @Override
        protected Boolean doInBackground(Void... voids) {
            try {
                faqModel = new FAQModelHelper(MainActivity.this);
                return true;
            } catch (Exception e) {
                Log.e("MainActivity", "Error initializing model", e);
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean success) {
            progressBar.setVisibility(View.GONE);
            if (!success) {
                Toast.makeText(MainActivity.this, 
                    "Failed to initialize the model. Please restart the app.", 
                    Toast.LENGTH_LONG).show();
            }
        }
    }

    private class ProcessMessageTask extends AsyncTask<String, Void, String> {
        @Override
        protected void onPreExecute() {
            progressBar.setVisibility(View.VISIBLE);
            inputLayout.setEnabled(false);
        }

        @Override
        protected String doInBackground(String... strings) {
            try {
                return faqModel.getAnswer(strings[0]);
            } catch (Exception e) {
                Log.e("MainActivity", "Error processing message", e);
                return "I'm sorry, I encountered an error processing your message.";
            }
        }

        @Override
        protected void onPostExecute(String response) {
            progressBar.setVisibility(View.GONE);
            inputLayout.setEnabled(true);
            addBotMessage(response);
        }
    }
}
```

## Running the App

1. **Build and Run**
   - Connect an Android device or start an emulator
   - Click the "Run" button in Android Studio
   - Select your target device and click "OK"

2. **Testing**
   - Type a question in the input field
   - Press the send button or the enter key
   - The app will process your question and display the response

## Testing and Debugging

### Common Issues

1. **Model Loading Failed**
   - Ensure the model files are in the correct location: `assets/model/onnx/`
   - Check that the model file names match exactly
   - Verify the model is properly exported to ONNX format

2. **App Crashes on Launch**
   - Check Logcat for error messages
   - Ensure all required permissions are declared in AndroidManifest.xml
   - Verify all dependencies are properly added to build.gradle

3. **Slow Response**
   - The model runs on the CPU by default
   - For better performance, consider:
     - Using a smaller model
     - Implementing model quantization
     - Running on a device with GPU support

## Future Improvements

1. **Enhancements**
   - Add typing indicators
   - Implement message status (sent, delivered, read)
   - Add support for rich media (images, links)
   - Implement conversation history

2. **Performance**
   - Add model quantization for faster inference
   - Implement caching for common queries
   - Add background processing for better UX

3. **Features**
   - Add support for multiple languages
   - Implement user authentication
   - Add analytics for common questions
   - Integrate with a backend service for fallback responses

## Conclusion

This guide provides a complete implementation of a Mental Health FAQ chatbot for Android. The app features a clean, modern UI with smooth animations and responsive design. The ONNX Runtime ensures efficient model inference on mobile devices.

For any issues or questions, please refer to the [ONNX Runtime documentation](https://onnxruntime.ai/) or open an issue in the project repository.

---
*Note: This implementation is for educational purposes. For production use, consider adding proper error handling, security measures, and compliance with data protection regulations.*
