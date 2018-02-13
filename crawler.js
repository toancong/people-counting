const fs = require('fs')
const request = require('request')
const GoogleImages = require('google-images')
const uuid = require('uuid/v4')
const async =  require('async')

const client = new GoogleImages('003826566325732178517:pvvwrqsyhcu', 'AIzaSyA0DBFC18ApswlgmxalxinpKLKnPPKH_9Y')
const download = (uri, filename, callback) => {
  request.head(uri, (err, res, body) => {
    if (err) {
        callback(err)
        return
    }

    request(uri).pipe(fs.createWriteStream(filename)).on('close', callback);
  })
}
const exec = (keyword, currentPage, toPage) => {
    console.log(keyword)
    const opts = {
        page: currentPage,
    }
    const path = storage + '/' + keyword
    if (!fs.existsSync(path)){
        fs.mkdirSync(path);
    }
    async.timesSeries(toPage - currentPage + 1, (i, next) => {
        const options = Object.assign({}, opts)
        options.page = i + currentPage
        console.log('Page: ' + options.page)
        client.search(keyword, options)
            .then(images => {
                async.eachOf(images, (img, j, cb) => {
                    try {
                        const savePath = path + '/' + options.page + '-' + j + '.JPEG'
                        download(img.url, savePath, () => {
                            console.log('Done ' + img.url)
                            cb()
                        })
                    } catch (err) {
                        console.log(err);
                        cb()
                    }
                }, (err) => {
                    console.log('Page: ' + options.page + ' done')
                    next()
                });
            })
            .catch(err => {
                console.log(err)
                next()
            })
    }, () => {
        console.log('Done');
    })
}

const storage = './train/Images'

exec('Hoc sinh', 1, 10)
