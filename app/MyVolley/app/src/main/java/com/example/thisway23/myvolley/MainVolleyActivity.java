package com.example.thisway23.myvolley;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.json.JSONException;
import org.json.JSONObject;


public class MainVolleyActivity extends ActionBarActivity implements Response.Listener,
        Response.ErrorListener {
    public static final String REQUEST_TAG = "MainVolleyActivity";
    private TextView mTextView;
    private Button mButton;
    private RequestQueue mQueue;
    private WebView browser;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_volley);

        mTextView = (TextView) findViewById(R.id.textView);
        mButton = (Button) findViewById(R.id.button);

        browser = (WebView)findViewById(R.id.webBrowser);
        browser.setWebViewClient(new WebBrowser());

        browser.getSettings().setLoadsImagesAutomatically(true);
        browser.getSettings().setJavaScriptEnabled(true);
        browser.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);

        //String url = "https://www.airbnb.com/rooms/6194193?checkin=5%2F2%2F2015&checkout=5%2F9%2F2015&s=GH-A";
        //browser.loadUrl(url);
    }

    @Override
    protected void onStart() {
        super.onStart();
        mQueue = CustomVolleyRequestQueue.getInstance(this.getApplicationContext())
                .getRequestQueue();
        //String url = "http://api.openweathermap.org/data/2.5/weather?q=London,uk";
        try {
            String url = "http://172.31.20.12:5000/messages";
            String json = "{\"id\":\"246030\",\"yr\":\"2015\", \"month\":\"05\", \"day\":\"16\", \"duration\":\"1\"}";

            JSONObject jsonObj = new JSONObject(json);

            final CustomJSONObjectRequest jsonRequest = new CustomJSONObjectRequest(Request.Method
                    .POST, url,
                    jsonObj, this, this);
            jsonRequest.setTag(REQUEST_TAG);

            mButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mQueue.add(jsonRequest);
                }
            });
        } catch (Exception e) {
            //Log.d("InputStream", e.getLocalizedMessage());
        }
    }

    @Override
    protected void onStop() {
        super.onStop();
        if (mQueue != null) {
            mQueue.cancelAll(REQUEST_TAG);
        }
    }

    @Override
    public void onErrorResponse(VolleyError error) {
        mTextView.setText(error.getMessage());
    }

    @Override
    public void onResponse(Object response) {
        try {
            //mTextView.setText(mTextView.getText() + "\n\n" + ((JSONObject) response).getString
            //        ("name"));
            JSONObject JSONObj = (JSONObject) response;
            mTextView.setText("price: " + JSONObj.getString("price") + "\n" +
                            "neighborhood: " + JSONObj.getString("neighborhood") + "\n" +
                            "rating:" + JSONObj.getString("rating") + "\n"
            );
            browser.loadUrl(JSONObj.getString("url"));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private class WebBrowser extends WebViewClient {

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            view.loadUrl(url);
            return true;
        }
    }
}