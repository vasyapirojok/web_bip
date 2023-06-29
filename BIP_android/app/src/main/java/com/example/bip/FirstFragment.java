package com.example.bip;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import com.example.bip.databinding.FragmentFirstBinding;
import com.example.bip.Communicator;

import okhttp3.OkHttpClient;
import okhttp3.Request;

public class FirstFragment extends Fragment {

    private FragmentFirstBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentFirstBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);



        binding.btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final int[] res = new int[1];
//                TODO: send creds, if error - print error, other way - to code page

                Thread thread = new Thread(new Runnable() {

                    @Override
                    public void run() {
                        try {
                            Communicator communicator = new Communicator();
                            res[0] = communicator.Login(binding.etEmail.getText().toString(), binding.etPassword.getText().toString());

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
                        case 2:
                            mBuilder.setMessage("Invalid credentials");
                            break;
                        default:
                            mBuilder.setMessage("Server error code: " + res[0]);
                    }
                    mBuilder.setPositiveButton("Ok", (dialog, which) -> {
                        // Continue with delete operation
                    });


                    AlertDialog mDialog = mBuilder.create();
                    mDialog.show();
                    return;
                }
                NavHostFragment.findNavController(FirstFragment.this)
                        .navigate(R.id.action_FirstFragment_to_code_fragment);
            }
        });

        binding.btnHaveAcc.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                NavHostFragment.findNavController(FirstFragment.this)
                        .navigate(R.id.action_FirstFragment_to_SecondFragment);
            }
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}