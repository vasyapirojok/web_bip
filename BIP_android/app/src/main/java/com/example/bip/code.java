package com.example.bip;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.bip.databinding.FragmentCodeBinding;
import com.example.bip.databinding.FragmentFirstBinding;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link code#} factory method to
 * create an instance of this fragment.
 */
public class code extends Fragment {

    private FragmentCodeBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentCodeBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);


        binding.btnSendCode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//              TODO: send and check code, if incorrect - to login page, other way - to shop page
                final int[] res = new int[1];
//              TODO: check passwords, send creds, if error - print error, other way - to login page
                Thread thread = new Thread(new Runnable() {

                    @Override
                    public void run() {
                        try {

                            Communicator communicator = new Communicator();
                            res[0] = communicator.VerifyCode(binding.etEmail.getText().toString(), binding.etCode.getText().toString());


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
                NavHostFragment.findNavController(code.this)
                        .navigate(R.id.action_CodeFragment_to_ChoiceFragment);
            }
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}