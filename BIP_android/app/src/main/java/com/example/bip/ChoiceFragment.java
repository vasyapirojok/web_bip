package com.example.bip;

import android.content.DialogInterface;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.bip.databinding.FragmentChoiceBinding;
import com.example.bip.databinding.FragmentCodeBinding;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link ChoiceFragment#} factory method to
 * create an instance of this fragment.
 */
public class ChoiceFragment extends Fragment {

    private FragmentChoiceBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentChoiceBinding.inflate(inflater, container, false);
        binding.daysPicker.setMinValue(1);
        binding.daysPicker.setMaxValue(100);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

//        TODO: check if jwt token is valid

        String[] listItems = getResources().getStringArray(R.array.shops_array);
        binding.shopResult.setText(listItems[0]);

        String[] listItemsEn = getResources().getStringArray(R.array.shops_array_en);
        final int[] index = {0};
        final JSONObject[] json = {null};

        binding.btnShop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                AlertDialog.Builder mBuilder = new AlertDialog.Builder(getActivity());
                mBuilder.setTitle("Choose a shop");

                mBuilder.setSingleChoiceItems(listItems, -1, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        binding.shopResult.setText(listItems[i]);
                        index[0] = i;
                        dialogInterface.dismiss();
                    }
                });

                AlertDialog mDialog = mBuilder.create();
                mDialog.show();
            }
        });

        binding.btnConf.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final int[] res = new int[1];
//                TODO: send creds, if error - print error, other way - to code page

                Thread thread = new Thread(new Runnable() {

                    @Override
                    public void run() {
                        try {
                            Communicator communicator = new Communicator();
                            res[0] = communicator.ReqRacio(Integer.parseInt(binding.etPrice.getText().toString()), binding.daysPicker.getValue(), listItemsEn[index[0]]);
                            json[0] = communicator.getJsonObject();

                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                });

                thread.start();
                try {
                    thread.join();
                } catch (Exception e) {
                    e.printStackTrace();
                }

                if (res[0] != 0 && res[0] != 200) {
                    androidx.appcompat.app.AlertDialog.Builder mBuilder = new androidx.appcompat.app.AlertDialog.Builder(getActivity());
                    mBuilder.setTitle("Error");
                    switch (res[0]) {
                        case 1:
                            mBuilder.setMessage("Unknown error");
                            break;
                        default:
                            mBuilder.setMessage("Server error code: " + res[0]);
                    }
                    mBuilder.setPositiveButton("Ok", (dialog, which) -> {
                        // Continue with delete operation
                    });


                    AlertDialog mDialog = mBuilder.create();
                    mDialog.show();
                }

//                generate string
                StringBuilder result = new StringBuilder();
                try {
                    JSONArray offer = json[0].getJSONArray("offer");
                    for(int i = 0; i < offer.length() && i < 17; i++) {
                        JSONObject obj = offer.getJSONObject(i);
                        result.append(obj.get("name").toString()).append(" ").append(obj.get("priceAfter").toString()).append("\n");

                        androidx.appcompat.app.AlertDialog.Builder mBuilder = new androidx.appcompat.app.AlertDialog.Builder(getActivity());
                        mBuilder.setTitle("Result");
                        mBuilder.setMessage(result);
                        mBuilder.setPositiveButton("Ok", (dialog, which) -> {
                            // Continue with delete operation
                        });


                        AlertDialog mDialog = mBuilder.create();
                        mDialog.show();
                    }
                }catch (Exception e) {
                    e.printStackTrace();
                }

            }
        });

    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}