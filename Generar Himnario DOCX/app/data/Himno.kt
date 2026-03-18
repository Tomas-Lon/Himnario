package com.tuapp.himnario.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "himnos")
data class Himno(
    @PrimaryKey val numero: Int,
    val titulo: String,
    val letra: String
)
