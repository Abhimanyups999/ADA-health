package com.example.aiswarya.mobilitymodel;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.preference.PreferenceManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

public class Custom_view_visited_game extends BaseAdapter {
    String[]gname,gamecode;
    private Context context;

    public Custom_view_visited_game(Context appcontext,String[]gname1,String[]gamecode)
    {
        this.context=appcontext;
        this.gname=gname1;
        this.gamecode=gamecode;



    }

    @Override
    public int getCount() {
        return gname.length;
    }

    @Override
    public Object getItem(int i) {
        return null;
    }

    @Override
    public long getItemId(int i) {
        return 0;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        LayoutInflater inflator=(LayoutInflater)context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);

        View gridView;
        if(view==null)
        {
            gridView=new View(context);
            //gridView=inflator.inflate(R.layout.customview, null);
            gridView=inflator.inflate(R.layout.custom_view_visited_game,null);

        }
        else
        {
            gridView=(View)view;

        }
        TextView tv1=(TextView)gridView.findViewById(R.id.textView16);
        ImageView im=(ImageView) gridView.findViewById(R.id.imageView10);

        tv1.setTextColor(Color.BLACK);


        tv1.setText(gname[i]);


        SharedPreferences sh= PreferenceManager.getDefaultSharedPreferences(context);
        String ip=sh.getString("ip","");

        String url="http://" + ip + ":5000/static/game/"+gamecode[i]+".jpg";


        Picasso.with(context).load(url).transform(new CircleTransform()). into(im);

        return gridView;
    }
}
