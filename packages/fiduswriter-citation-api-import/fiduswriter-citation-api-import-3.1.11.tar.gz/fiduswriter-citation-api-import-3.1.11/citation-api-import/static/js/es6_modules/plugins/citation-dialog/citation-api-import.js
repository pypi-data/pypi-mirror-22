import {setCheckableLabel} from "../../common"
import {BibLatexApiImporter} from "../../citation-api-import"

export class BibLatexApiImporterCitationDialog {
    constructor(citationDialog) {
        this.citationDialog = citationDialog
    }

    init() {
        this.addButton()
        this.bind()
    }

    addButton() {
        let buttonHTML = `
            <button type="button" class="fw-button fw-light fw-add-button
                    register-new-bib-source import-api
                    ui-button ui-corner-all ui-widget">
                ${gettext('Import from database')}
            </button>`
        jQuery('button.register-new-bib-source').after(buttonHTML)
    }

    bind() {
        //import via web api

        jQuery('.import-api').bind('click', () => {
            let apiImporter = new BibLatexApiImporter(
                this.citationDialog.editor.bibDB,
                bibEntries => {
                    this.citationDialog.addToCitableItems(bibEntries)
                    jQuery('.fw-checkable').unbind('click')
                    jQuery('.fw-checkable').bind('click', function() {
                        setCheckableLabel(jQuery(this))
                    })
                }
            )

            apiImporter.init()
        })
    }
}
