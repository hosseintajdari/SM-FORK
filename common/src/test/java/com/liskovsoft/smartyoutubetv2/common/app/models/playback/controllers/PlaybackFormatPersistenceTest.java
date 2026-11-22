package com.liskovsoft.smartyoutubetv2.common.app.models.playback.controllers;

import com.liskovsoft.smartyoutubetv2.common.exoplayer.selector.ExoFormatItem;
import com.liskovsoft.smartyoutubetv2.common.exoplayer.selector.FormatItem;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.annotation.Config;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = 28)
public class PlaybackFormatPersistenceTest {
    @Test
    public void persianSubtitleLanguageSurvivesSettingsReload() {
        FormatItem persian = ExoFormatItem.fromSubtitleParams("fa");
        FormatItem restored = ExoFormatItem.from(persian.toString());

        assertEquals(FormatItem.TYPE_SUBTITLE, restored.getType());
        assertEquals("fa", restored.getLanguage());
        assertFalse(restored.isDefault());
    }

    @Test
    public void disabledSubtitlesStayDisabledAfterSettingsReload() {
        FormatItem restored = ExoFormatItem.from(FormatItem.SUBTITLE_NONE.toString());

        assertEquals(FormatItem.TYPE_SUBTITLE, restored.getType());
        assertTrue(restored.isDefault());
    }

    @Test
    public void highestBitrateAudioSurvivesSettingsReload() {
        ExoFormatItem restored = ExoFormatItem.from(FormatItem.AUDIO_HIGHEST_BITRATE.toString());

        assertEquals(FormatItem.TYPE_AUDIO, restored.getType());
        assertEquals(FormatItem.HIGHEST_AUDIO_BITRATE, restored.getTrack().format.bitrate);
    }
}
