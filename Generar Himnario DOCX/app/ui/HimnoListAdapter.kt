package com.tuapp.himnario.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.tuapp.himnario.data.Himno
import com.tuapp.himnario.databinding.ItemHimnoBinding

class HimnoListAdapter(
    private val himnos: List<Himno>,
    private val onClick: (Himno) -> Unit
) : RecyclerView.Adapter<HimnoListAdapter.HimnoViewHolder>() {

    inner class HimnoViewHolder(val binding: ItemHimnoBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): HimnoViewHolder {
        val binding = ItemHimnoBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return HimnoViewHolder(binding)
    }

    override fun onBindViewHolder(holder: HimnoViewHolder, position: Int) {
        val himno = himnos[position]
        holder.binding.titulo.text = "${himno.numero}. ${himno.titulo}"
        holder.binding.root.setOnClickListener { onClick(himno) }
    }

    override fun getItemCount() = himnos.size
}
