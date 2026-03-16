tell application "QLab"
    set midiDevice to 1
    set channelsToUnmute to {{CHANNELS_TO_UNMUTE}}
    set ensembleChannels to {{CHANNELS_ENSEMBLE_BUS}}
    set totalChannels to {{MAX_CHANNELS}}

    make front workspace type "Group"
    set groupCue to last item of (selected of front workspace as list)

    tell groupCue
        set q name to "{{CUE_NAME}}"
        set q number to "{{CUE_NUMBER}}"
    end tell

    repeat with ch from 1 to totalChannels
        set formattedCh to (do shell script "printf '%x\n' " & (ch - 1))
        
        make front workspace type "Network"
        set targetCue to last item of (selected of front workspace as list)
        if targetCue is not missing value then
            tell targetCue
                set network patch number to {{NETWORK_PATCH}}

                if ch is in channelsToUnmute then
                    set custom message to "B" & formattedCh & " 63 00 B" & formattedCh & " 62 00 B" & formattedCh & " 06 00 B" & formattedCh & " 26 01"
                else
                    set custom message to "B" & formattedCh & " 63 00 B" & formattedCh & " 62 00 B" & formattedCh & " 06 00 B" & formattedCh & " 26 00"
                end if

                set q number to ""

                if ch is in channelsToUnmute then
                    set q name to "Channel " & ch & " Unmute"
                else
                    set q name to "Channel " & ch & " Mute"
                end if
            end tell

            move targetCue to end of groupCue
        end if
    end repeat

    repeat with ch from 1 to totalChannels
        set formattedCh to (do shell script "printf '%x\n' " & (ch - 1))
        if ensembleChannels is not missing value then
            make front workspace type "Network"
            set targetDcaCue to last item of (selected of front workspace as list)

            if targetDcaCue is not missing value then
                tell targetDcaCue
                    set network patch number to {{NETWORK_PATCH}}

                    if ch is in ensembleChannels then
                        set bitmask to 3
                        set custom message to "/ch/" & formattedCh & "/mix/grp/dca " & bitmask
                    else
                        set bitmask to 1
                        set custom message to "/ch/" & formattedCh & "/mix/grp/dca " & bitmask
                    end if

                    set q number to ""

                    if ch is in ensembleChannels then
                        set q name to "Channel " & ch & " Ensemble On"
                    else
                        set q name to "Channel " & ch & " Ensemble Off"
                    end if
                end tell

                move targetDcaCue to end of groupCue
            end if
        end if
    end repeat
end tell