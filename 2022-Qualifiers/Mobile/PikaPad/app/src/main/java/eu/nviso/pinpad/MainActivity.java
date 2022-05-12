package eu.nviso.pinpad;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.Toast;

import com.goodiebag.pinview.Pinview;

public class MainActivity extends AppCompatActivity implements Pinview.PinViewEventListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Pinview pin = (Pinview) findViewById(R.id.pinview);
        pin.requestPinEntryFocus();
            pin.setPinViewEventListener(this);


    }

    @Override
    public void onDataEntered(Pinview pinview, boolean fromUser) {
        String pincode = pinview.getValue();
        String firstPart = pincode.substring(0, 3);
        String secondPart = pincode.substring(2, 5);
        String thirdPart = pincode.substring(4, 6);

        // 274169
        // first = 274
        // second = 416
        // third = 69

        if( Integer.parseInt(firstPart) * 7 == 1918 && Integer.parseInt(secondPart) >> 3 == 52 && Integer.parseInt(thirdPart) << 5 == 2208)
        {
            String[] flags = getResources().getStringArray(R.array.flags);
            String flag = flags[Integer.parseInt(firstPart) + Integer.parseInt(secondPart) + Integer.parseInt(thirdPart)];
            Toast.makeText(this.getApplicationContext(), "You caught a " + flag, Toast.LENGTH_LONG).show();
        }
        else{
            Toast.makeText(this.getApplicationContext(), "Wild Pokemon fled...", Toast.LENGTH_LONG).show();
            pinview.clearValue();
        }

    }
}