package com.tuapp.himnario.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [Himno::class], version = 1)
abstract class HimnoDatabase : RoomDatabase() {
    abstract fun himnoDao(): HimnoDao

    companion object {
        @Volatile private var INSTANCE: HimnoDatabase? = null

        fun getDatabase(context: Context): HimnoDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    HimnoDatabase::class.java,
                    "himnario.sqlite"
                )
                .createFromAsset("himnario.sqlite")
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
