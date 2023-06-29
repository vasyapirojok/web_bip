package com.example.bip;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.bip.databinding.FragmentCodeBinding;
import com.example.bip.databinding.FragmentListBinding;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link ListFragment#} factory method to
 * create an instance of this fragment.
 */
public class ListFragment extends Fragment {

    private FragmentListBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentListBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

//        TODO: check if jwt token is valid


    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}