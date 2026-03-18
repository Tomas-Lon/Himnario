package com.tuapp.himnario

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.tuapp.himnario.data.HimnoDatabase
import com.tuapp.himnario.databinding.ActivityMainBinding
import com.tuapp.himnario.ui.HimnoListAdapter
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val db = HimnoDatabase.getDatabase(this)
        lifecycleScope.launch {
            val himnos = db.himnoDao().getAll()
            binding.recyclerView.layoutManager = LinearLayoutManager(this@MainActivity)
            binding.recyclerView.adapter = HimnoListAdapter(himnos) { himno ->
                // TODO: abrir detalle
            }
        }
    }
}
