import {BibLatexApiImporter} from "../../citation-api-import"

export class BibLatexApiImporterBibliographyOverview {
    constructor(bibliographyOverview) {
        this.bibliographyOverview = bibliographyOverview
    }

    init() {
        this.addButton()
        this.bind()
    }

    addButton() {
        let buttonHTML = `<li class="fw-document-menu-item">
            <span class="import-api fw-button fw-light fw-large">
                ${gettext("Import from Database")}
                <span class="icon-plus-circle"></span>
            </span>
        </li>`
        jQuery('ul.fw-document-menu').append(buttonHTML)
    }

    bind() {
        //import via web api
        jQuery('.import-api').bind('click', () => {
            let apiImporter = new BibLatexApiImporter(
                this.bibliographyOverview.bibDB,
                bibEntries => this.bibliographyOverview.addBibList(bibEntries)
            )
            apiImporter.init()
        })
    }
}
