/** @odoo-module **/
import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { onMounted, onWillUnmount } from "@odoo/owl";

const AUTO_SAVE_MODELS = ["sale.order", "purchase.order"];
const INITIAL_DELAY = 120000; // 2 minutes
const REGULAR_INTERVAL = 240000; // 4 minutes

patch(FormController.prototype, {
    setup() {
        super.setup();
        this._autoSaveTimer = null;
        this._isFirstSave = true;
        this._partnerWatcherActive = false;

        onMounted(() => {
            if (AUTO_SAVE_MODELS.includes(this.props.resModel)) {
                const record = this.model.root;
                
                // For new records, watch partner_id field
                if (!record.resId) {
                    this._watchPartnerField();
                } else {
                    // For existing records, start auto-save immediately
                    this._startAutoSave(INITIAL_DELAY);
                }
            }
        });

        onWillUnmount(() => {
            this._clearAutoSaveTimer();
        });
    },

    _watchPartnerField() {
        if (this._partnerWatcherActive) return;
        this._partnerWatcherActive = true;

        const record = this.model.root;
        
        // Watch for changes using model's update mechanism
        const originalUpdate = record.update.bind(record);
        record.update = async (changes) => {
            const result = await originalUpdate(changes);
            
            // Check if partner_id was set
            if (changes.partner_id && !record.resId) {
                const partnerId = Array.isArray(changes.partner_id) 
                    ? changes.partner_id[0] 
                    : changes.partner_id;
                
                if (partnerId) {
                    console.log("partner_id set, saving new record...");
                    setTimeout(() => this._saveNewRecord(), 100); // Small delay for other onchanges
                }
            }
            
            return result;
        };
    },

    async _saveNewRecord() {
        const record = this.model?.root;
        if (!record || record.resId) return; // Already saved
        
        try {
            await record.save({ stayInEdition: true });
            console.log("New record saved:", record.resId);
            
            // Start auto-save timer after first save
            this._isFirstSave = false;
            this._partnerWatcherActive = false; // Stop watching
            this._startAutoSave(REGULAR_INTERVAL);
        } catch (error) {
            console.warn("Failed to save new record:", error);
        }
    },

    _startAutoSave(interval) {
        this._clearAutoSaveTimer();
        this._autoSaveTimer = setInterval(() => {
            this._autoSave();
        }, interval);
        console.log("Auto-save timer started:", interval / 1000, "seconds");
    },

    _clearAutoSaveTimer() {
        if (this._autoSaveTimer) {
            clearInterval(this._autoSaveTimer);
            this._autoSaveTimer = null;
        }
    },

    async _autoSave() {
        const record = this.model?.root;
        if (!record || !record.resId) return;
        if (!record.isDirty) return; // No changes
        if (record.data.state && record.data.state !== "draft") return;

        try {
            await record.save({ stayInEdition: true });
            console.log("Auto-saved:", this.props.resModel, record.resId);
        } catch (error) {
            console.warn("Auto-save failed:", error);
        }
    },
});
