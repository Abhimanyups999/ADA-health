package com.example.lenovo.smart_home;

import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.Map;

public class Upload_our_design extends AppCompatActivity implements View.OnClickListener {
EditText ed15,ed16,ed17,ed14;
    Button browse,upload;
    Spinner sp;

    String path, atype, fname, attach, attatch1;
    byte[] byteArray = null;
    String url3="";
    String[]dis={"--select--","Architect","furniture_designer","interiors"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_upload_our_design);

        ed17=(EditText)findViewById(R.id.editText17);
        ed14=(EditText)findViewById(R.id.editText14);
        ed16=(EditText)findViewById(R.id.editText16);
        ed15=(EditText)findViewById(R.id.editText15);


        sp=(Spinner)findViewById(R.id.spinner2);
        ArrayAdapter<String> ad=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,dis);
        sp.setAdapter(ad);

       browse=(Button) findViewById(R.id.button6);
        browse.setOnClickListener(this);
       upload=(Button) findViewById(R.id.button14);
        upload.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        if (view == browse) {
            showfilechooser(1);
        }

        if (view == upload) {

            final SharedPreferences sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
            String ip = sh.getString("ip", "");
            final String uid = sh.getString("user", "");
            final String type = sp.getSelectedItem().toString();
            final String pname = ed16.getText().toString();
            final String dis = ed17.getText().toString();
            final String amount = ed14.getText().toString();
            //Toast.makeText(getApplicationContext(),uid+"/"+type+"/"+pname+"/"+dis+"/"+amount+"/"+attach,Toast.LENGTH_SHORT).show();
            if (pname.equalsIgnoreCase("")) {
                ed16.setError("Null");
            }
            if (dis.equalsIgnoreCase("")) {
                ed17.setError("Null");
            }
            if (amount.equalsIgnoreCase("")) {
                ed14.setError("Null");
            } else {
                url3 = "http://" + ip + ":5000/upload_cus_plan";
                RequestQueue requestqueue = Volley.newRequestQueue(getApplicationContext());

                StringRequest postrequest = new StringRequest(Request.Method.POST, url3, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String s) {

                        try {
                            JSONObject json = new JSONObject(s);
                            String res = json.getString("status");

                            if (res.equals("ok") == true) {

                                Toast.makeText(getApplicationContext(), "You have successfully shared", Toast.LENGTH_SHORT).show();
                                Intent i = new Intent(getApplicationContext(), View_my_plans.class);
                                startActivity(i);

                            } else {
                                Toast.makeText(getApplicationContext(), "You entered an invalid email or password ", Toast.LENGTH_SHORT).show();
                            }


                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError volleyError) {

                        Toast.makeText(getApplicationContext(), "Error" + volleyError.toString(), Toast.LENGTH_SHORT).show();


                    }
                }) {

                    @Override
                    public Map<String, String> getParams() {

                        Map<String, String> params = new HashMap<String, String>();
                        params.put("type", type);
                        params.put("uid", uid);
                        params.put("image", attach);
                        params.put("pname", pname);
                        params.put("disc", dis);
                        params.put("amount", amount);


                        return (params);

                    }
                };

                requestqueue.add(postrequest);


            }

        }
    }
    void showfilechooser(int string) {
        // TODO Auto-generated method stub
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        //getting all types of files

        intent.setType("*/*");
        intent.addCategory(Intent.CATEGORY_OPENABLE);

        try {
            startActivityForResult(Intent.createChooser(intent, "Select a File to Upload"), string);
        } catch (android.content.ActivityNotFoundException ex) {
            // Potentially direct the user to the Market with a Dialog
            Toast.makeText(getApplicationContext(), "Please install a File Manager.", Toast.LENGTH_SHORT).show();

        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (resultCode == RESULT_OK) {
            if (requestCode == 1) {
                ////
                Uri uri = data.getData();

                try {
                    path = FileUtils.getPath(this, uri);

                    File fil = new File(path);
                    float fln = (float) (fil.length() / 1024);
                    atype = path.substring(path.lastIndexOf(".") + 1);


                    fname = path.substring(path.lastIndexOf("/") + 1);
                    ed15.setText(fname);
                } catch (URISyntaxException e) {
                    e.printStackTrace();
                }

                try {

                    File imgFile = new File(path);

                    if (imgFile.exists()) {

                        Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
                        //i1.setImageBitmap(myBitmap);

                    }


                    File file = new File(path);
                    byte[] b = new byte[8192];
                    Log.d("bytes read", "bytes read");

                    InputStream inputStream = new FileInputStream(file);
                    ByteArrayOutputStream bos = new ByteArrayOutputStream();

                    int bytesRead = 0;

                    while ((bytesRead = inputStream.read(b)) != -1) {
                        bos.write(b, 0, bytesRead);
                    }
                    byteArray = bos.toByteArray();

                    String str = Base64.encodeToString(byteArray, Base64.NO_WRAP);
                    attach = str;


                } catch (Exception e) {
                    Toast.makeText(this, "String :" + e.getMessage().toString(), Toast.LENGTH_LONG).show();
                }

                ///

            }
        }

    }
}
