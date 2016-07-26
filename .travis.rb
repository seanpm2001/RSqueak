require "net/http"
require "pp"
require "travis/client"
require "active_support"
require "active_support/core_ext/numeric"
require "active_support/core_ext/date"
require "active_support/core_ext/time"

CODESPEED = URI("http://lively-kernel.org/codespeed")

client = Travis::Client.new(access_token: ENV["TRAVIS_API_TOKEN"])
repo = client.repo(ENV["REPOSITORY"])
vm = ENV["VM"]

yesterdays_builds = []
repo.builds.each do |b|
  break if (b.finished_at && b.finished_at < 1.day.ago)
  yesterdays_builds << b if b.passed?
end

yesterdays_builds.group_by do |b|
  b.commit.branch
end.each_pair do |branch, builds|
  last_build = builds.first
  commitdate = last_build.commit.committed_at
  commitver = ("%4s%2s%2s%2s%2s" % [commitdate.year, commitdate.month, commitdate.day,
                                    commitdate.hour, commitdate.min]).gsub(" ", "0")
  Net::HTTP.start(CODESPEED.host, CODESPEED.port) do |http|

    req = Net::HTTP::Post.new(CODESPEED.path)
    req["commitid"] = (ENV["USE_SHA"] ? last_build.commit.sha : commitver)
    req["branch"] = branch
    req["vm"] = vm

    req2 = Net::HTTP::Post.new(CODESPEED.path)
    req2["commitid"] = (ENV["USE_SHA"] ? last_build.commit.sha : commitver)
    req2["branch"] = branch
    req2["vm"] = "#{vm}64"

    begin
      puts "#{req["commitid"]}, #{req["branch"]}, #{req["vm"]}"
      http.request(req)
    rescue
      puts "Failed"
    end
    begin
      puts "#{req2["commitid"]}, #{req2["branch"]}, #{req2["vm"]}"
      http.request(req2)
    rescue
      puts "Failed"
    end
  end
end
