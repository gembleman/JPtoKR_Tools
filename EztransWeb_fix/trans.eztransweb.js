var trans = trans || {};
trans.eztransweb = new TranslatorEngine({
	id:"eztransweb",
	name:"ezTransXP Web",
	author:"REMEDY",
	version:"1.0",
	description:"ezTransXP translator API.",
	delimiter:"\n\n",
    lineSubstitute : '¶', //¶	
	targetUrl: 'http://127.0.0.1:5000/translate',
	maxRequestLength: 2000,
    batchDelay: 0.1,
	languages:{
		"jp":"Japanese",
		"kr":"Korean",
	},
	optionsForm:{
	  "schema": {
		"targetURL": {
		  "type": "string",
		  "title": "Target URL",
		  "description": "Translator target URL",
		  "default":"http://127.0.0.1:5000/translate",
		  "required":true
		}
    },
	  "form": [
		{
		  "key": "targetURL",
		  "onChange": function (evt) {
			var value = $(evt.target).val();
			trans.eztransweb.update("targetUrl", value);
		  }
		}		
	  ]
	}
});


trans.eztransweb.generateLangCode = function(langCode) {
	var language = {
		"jp":{"code":"jp","lang":"Japanese"},
		"kr":{"code":"kr","lang":"Korean"},	
	}
	
	if (Boolean(language[langCode]) == false) return 'auto';
	return language[langCode].code||false;
}


trans.eztransweb.onResponse = function(e) {
	console.log(e);
}


trans.eztransweb.translate = async function(text, options) {
    if (trans.eztransweb.isDisabled == true) return false;
    if (typeof text=='undefined') return text;
	var thisTranslator = this;

	var originalText = text;
    options = options||{};
    // try to load saved configuration
    try {
        var savedSL = trans.getSl();
        var savedTL = trans.getTl();
    } catch(e) {
        var savedSL = undefined;
        var savedTL = undefined;
    }
    options.sl = options.sl||savedSL||'ja';
    options.tl = options.tl||savedTL||'en';
    options.onAfterLoading = options.onAfterLoading||function() {};
    options.onError = options.onError||function() {};
    options.always = options.always||function() {};
 
    options.agressiveSplitting = true;
   
    let tStrings = [];
    let dict = new TranslationDictionary();
    
    var lineSubstitute = trans.eztransweb.lineSubstitute;
    if (options.agressiveSplitting && options.sl == "ja") {
        if (typeof text == "string") {
            text = [text]
        } else if (!Array.isArray(text)) {
            console.warn("Invalid text translation requested.", text);
            return text;
        }
       
       
        for (let i = 0; i < text.length; i++) {
            let tString = new TranslationString(text[i]);
            tStrings.push(tString);
            tString.addTranslatables(dict);
        }
       
        var newText = [];
        text = dict.symbols;
        for (var i=0; i<text.length; i++) {
            newText.push(str_ireplace(thisTranslator.delimiter, lineSubstitute, text[i]));
        }
        text = newText;
        text = text.join(thisTranslator.delimiter);
    } else {
   
        if (typeof text == "string") {
            text = str_ireplace(thisTranslator.delimiter, lineSubstitute, text);
        }
       
        if (Array.isArray(text)) {
            var newText = [];
            for (var i=0; i<text.length; i++) {
                newText.push(str_ireplace(thisTranslator.delimiter, lineSubstitute, text[i]));
            }
            text = newText;
            text = text.join(thisTranslator.delimiter);
        }
    }

    thisTranslator.isTranslating = true;
	thisTranslator.targetUrl = thisTranslator.targetUrl||'http://127.0.0.1:5000/translate';
    
    var theText = text;
    
    var formData = new FormData();
    formData.append("text", theText);
	
    return new Promise((resolve, reject) => {
        //var theText = trans.papago.escapeCharacter(text);
        $.ajax({
            url: thisTranslator.targetUrl,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            cache: false
        })    
        .done(function(data) {
            // alert(data);
            console.log("translating done : ");
            console.log(data);
            // alert(data);
            var translatedText = data;
            
            var result = {
                'sourceText':"",
                'translationText': translatedText,
                'source':[],
                'translation':[]
            };
            
            var dataSplit = translatedText.split(thisTranslator.delimiter);
            console.log(dataSplit);
            /*
            for (var i=0; i<data[0].length; i++) {
                result.sourceText += data[0][i][1];
                result.translationText += data[0][i][0];
            }
            */
            if (options.agressiveSplitting && options.sl == "ja") {
            
                //let tStrings = [];
                //let dict = new TranslationDictionary();
                console.log("dict: ");
                console.log(dict);
                for (let i = 0; i < dataSplit.length; i++) {
                    dict.addIndexedTranslation(i, dataSplit[i].replace(/\n/ig, ' '));
                }
                console.log(dict);
                console.log("tStrings:");
                console.log(tStrings);
                for (let i = 0; i < tStrings.length; i++) {
                    result.source.push (tStrings[i].originalString);
                    result.translation.push (tStrings[i].getTranslatedString(dict));
                }
                console.log(tStrings);
                
            } else {
                // result.translationText = fixTranslationFormatting(result.translationText);
                result.translationText = trans.eztransweb.unescapeCharacter(result.translationText);
                result.source = result.sourceText.split(thisTranslator.delimiter);
                result.translation = result.translationText.split(thisTranslator.delimiter);
                // restore escaped line from original text
                var tempArray = [];
                for (var i=0; i<result.source.length; i++) {
                    tempArray.push(str_ireplace(lineSubstitute, thisTranslator.delimiter, result.source[i]))
                }
                result.source = tempArray;
            
                var tempArray = [];
                for (var i=0; i<result.translation.length; i++) {
                    tempArray.push(str_ireplace(lineSubstitute, thisTranslator.delimiter, result.translation[i]))
                }
                result.translation = tempArray;
            }
        
            console.log(result);
            if (typeof options.onAfterLoading == 'function') {
                options.onAfterLoading.call(trans.eztransweb, result, data);
            }
        
            trans.eztransweb.isTranslating = false;
            resolve(result);
        })
        .always(function() {
            trans.eztransweb.isTranslating = false;
        })
        .error(function(evt, type, errorType) {
            console.log(arguments);
            trans.eztransweb.isTranslating = false;
            console.log("error translating text");
            if (typeof options.onError == 'function') {
                options.onError.call(trans.eztransweb, evt, type, errorType);
            }
            reject();
        }) 
    })
}


$(document).ready(function() {
	trans.eztransweb.init();
});
