package com.example.bip;

import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import com.example.bip.databinding.FragmentSecondBinding;

public class SecondFragment extends Fragment {

    private FragmentSecondBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentSecondBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

//        TODO: check if jwt token is valid

        binding.btnHaveAcc.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                NavHostFragment.findNavController(SecondFragment.this)
                        .navigate(R.id.action_SecondFragment_to_FirstFragment);
            }
        });

        binding.btnRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final int[] res = new int[1];
//              TODO: check passwords, send creds, if error - print error, other way - to login page
                Thread thread = new Thread(new Runnable() {

                    @Override
                    public void run() {
                        try {

//                            check passwords are same
                            if (!binding.etPassword.getText().toString().equals(binding.etRepassword.getText().toString())) {
                                return;
                            }

                            Communicator communicator = new Communicator();
                            res[0] = communicator.Register(binding.etEmail.getText().toString(), binding.etPassword.getText().toString());


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
                            mBuilder.setMessage("Email are already in use");
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
                NavHostFragment.findNavController(SecondFragment.this)
                        .navigate(R.id.action_SecondFragment_to_FirstFragment);
            }
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}