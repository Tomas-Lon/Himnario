package com.tuapp.himnario.data

import androidx.room.Dao
import androidx.room.Query

@Dao
interface HimnoDao {
    @Query("SELECT * FROM himnos ORDER BY numero")
    suspend fun getAll(): List<Himno>

    @Query("SELECT * FROM himnos WHERE numero = :num")
    suspend fun getByNumero(num: Int): Himno

    @Query("SELECT * FROM himnos WHERE titulo LIKE '%' || :query || '%' OR letra LIKE '%' || :query || '%'")
    suspend fun search(query: String): List<Himno>
}
